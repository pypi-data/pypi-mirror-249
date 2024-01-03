import random
from contextlib import asynccontextmanager
from typing import Union

import asyncpg


class UnsafeCRUDError(Exception):
    def __init__(self, query, params=None):
        self.query = query
        self.params = params
        self.unsafe_part = self._detect_unsafe_part()
        self.message = self._build_error_message()

    def _detect_unsafe_part(self):
        unsafe_keywords = ["DELETE", "DROP", "TRUNCATE", "ALTER"]
        for keyword in unsafe_keywords:
            if keyword in self.query.upper():
                return keyword
        return None

    def _build_error_message(self):
        params_info = f" with parameters: {self.params}" if self.params else ""
        unsafe_info = (
            f"Unsafe keyword detected: {self.unsafe_part}"
            if self.unsafe_part
            else "Unknown unsafe operation"
        )
        return f"Unsafe query detected: {self.query}{params_info}. {unsafe_info}. This query may pose a security risk."

    def __str__(self):
        return self.message


class DictRecord(asyncpg.Record):
    def __repr__(self):
        return self.as_dict().__repr__()

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )

    def __getitem__(self, key):
        result = super().__getitem__(key)
        return dict(result) if isinstance(result, asyncpg.Record) else result

    def as_dict(self):
        return dict(self.items())


# noinspection PyArgumentList
class AsyncPGCRUD:
    """
    Asynchronous PostgreSQL CRUD operations.

    :param connection_params: A dictionary containing connection parameters.
    :type connection_params: dict
    :param table_name: The name of the table to perform CRUD operations on.
    :type table_name: str
    :param columns: A dictionary mapping column names to their data types.
    :type columns: dict
    """

    def __init__(self, connection_params: dict, table_name: str, columns: dict):
        """
        Initialize the AsyncPGCRUD instance.

        :param connection_params: A dictionary containing connection parameters.
        :type connection_params: dict
        :param table_name: The name of the table to perform CRUD operations on.
        :type table_name: str
        :param columns: A dictionary mapping column names to their data types.
        :type columns: dict
        """
        self.connection_params = connection_params
        self.connection_params["record_class"] = DictRecord
        self.table_name = table_name
        self.columns = columns

    @asynccontextmanager
    async def _get_connection_cursor(self):
        """
        Asynchronous context manager for acquiring a connection and cursor.

        :return: An asyncpg database connection.
        :rtype: asyncpg.Connection
        """
        connection = await asyncpg.connect(**self.connection_params)
        try:
            async with connection.transaction():
                yield connection
        finally:
            await connection.close()

    async def create_table(self):
        """
        Create the table if it does not exist.
        """
        create_table_query = (
            f"CREATE TABLE IF NOT EXISTS {self.table_name} "
            f"({', '.join([f'{col} {data_type}' for col, data_type in self.columns.items()])})"
        )

        async with self._get_connection_cursor() as connection:
            await connection.execute(create_table_query)

    def _build_insert_query(self, data):
        """
        Build an insert query for the given data.

        :param data: A dictionary of column-value pairs.
        :type data: dict
        :return: The insert query and its parameters.
        :rtype: tuple
        """
        columns = data.keys()
        values = data.values()
        return (
            f"INSERT INTO {self.table_name} "
            f"({', '.join(columns)}) VALUES ({', '.join(['$' + str(i + 1) for i in range(len(values))])})"
        ), tuple(values)

    async def create(self, data):
        """
        Create a new record in the table.

        :param data: A dictionary of column-value pairs.
        :type data: dict
        """
        insert_query, params = self._build_insert_query(data)
        async with self._get_connection_cursor() as connection:
            await connection.execute(insert_query, *params)

    def _build_select_query(self, conditions=None, columns_clause="*"):
        """
        Build a select query with optional conditions.

        :param conditions: A dictionary of column-value pairs for the WHERE clause.
        :type conditions: dict, optional
        :param columns_clause: The columns to select in the query.
        :type columns_clause: str, optional
        :return: The select query and its parameters.
        :rtype: tuple
        """
        conditions = conditions or {}
        where_conditions = (
            (
                "WHERE "
                + " AND ".join(
                    [f"{key} = ${i + 1}" for i, key in enumerate(conditions)]
                )
            )
            if conditions
            else ""
        )

        query = f"SELECT {columns_clause} FROM {self.table_name} {where_conditions}"
        params = list(conditions.values()) if conditions else None

        return query, params

    async def read_all(self):
        """
        Read all records from the table.

        :return: A list of records.
        :rtype: list
        """
        select_query, params = self._build_select_query()
        async with self._get_connection_cursor() as connection:
            return await connection.fetch(select_query, *params if params else [])

    async def read(self, conditions):
        """
        Read a record from the table based on the given conditions.

        :param conditions: A dictionary of column-value pairs for the WHERE clause.
        :type conditions: dict
        :return: The matching record.
        :rtype: dict
        """
        select_query, params = self._build_select_query(conditions)
        async with self._get_connection_cursor() as connection:
            return await connection.fetchrow(select_query, *params)

    async def read_columns(self, conditions, columns=None):
        """
        Read specific columns from a record based on the given conditions.

        :param conditions: A dictionary of column-value pairs for the WHERE clause.
        :type conditions: dict
        :param columns: A list of columns to select in the query.
        :type columns: list, optional
        :return: The record with the selected columns.
        :rtype: dict
        """
        columns_clause = ", ".join(columns) if columns else "*"
        select_query, params = self._build_select_query(conditions, columns_clause)
        async with self._get_connection_cursor() as connection:
            return await connection.fetchrow(select_query, *params)

    def _build_update_query(self, data, conditions):
        """
        Build an update query for the given data and conditions.

        :param data: A dictionary of column-value pairs to update.
        :type data: dict
        :param conditions: A dictionary of column-value pairs for the WHERE clause.
        :type conditions: dict
        :return: The update query and its parameters.
        :rtype: tuple
        """
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(data)])
        where_conditions = ", ".join(
            [f"{key} = ${i + len(data) + 1}" for i, key in enumerate(conditions)]
        )

        return (
            f"UPDATE {self.table_name} SET {set_clause} WHERE {where_conditions}"
        ), list(data.values()) + list(conditions.values())

    async def update(self, data, conditions):
        """
        Update records in the table based on the given data and conditions.

        :param data: A dictionary of column-value pairs to update.
        :type data: dict
        :param conditions: A dictionary of column-value pairs for the WHERE clause.
        :type conditions: dict
        """
        update_query, params = self._build_update_query(data, conditions)
        async with self._get_connection_cursor() as connection:
            await connection.execute(update_query, *params)

    def _build_delete_query(self, conditions):
        """
        Build a delete query based on the given conditions.

        :param conditions: A dictionary of column-value pairs for the WHERE clause.
        :type conditions: dict
        :return: The delete query and its parameters.
        :rtype: tuple
        """
        where_conditions = ", ".join(
            [f"{key} = ${i + 1}" for i, key in enumerate(conditions)]
        )

        return (f"DELETE FROM {self.table_name} WHERE {where_conditions}"), list(
            conditions.values()
        )

    async def delete(self, conditions):
        """
        Delete records from the table based on the given conditions.

        :param conditions: A dictionary of column-value pairs for the WHERE clause.
        :type conditions: dict
        """
        delete_query, params = self._build_delete_query(conditions)
        async with self._get_connection_cursor() as connection:
            await connection.execute(delete_query, *params)

    async def get_random_item(self):
        """
        Get a random record from the table.

        :return: A random record.
        :rtype: dict
        """
        count_query = f"SELECT COUNT(*) FROM {self.table_name}"

        async with self._get_connection_cursor() as connection:
            total_rows = await connection.fetchval(count_query)

            if total_rows > 0:
                random_offset = random.randint(0, total_rows - 1)
                select_query = f"SELECT * FROM {self.table_name} OFFSET $1 LIMIT 1"
                return await connection.fetchrow(select_query, random_offset)
            else:
                return None

    async def execute_query(
        self,
        query: str,
        params: Union[None, tuple] = None,
        fetch_result: bool = False,
        unsafe: bool = False,
    ):
        """
        Execute a custom SQL query using prepared statements.

        :param unsafe : If True, execute the query without sanitizing the parameters.
        :param query: SQL query string with placeholders for parameters.
        :param params: Tuple of parameters for the query (default is None).
        :param fetch_result: If True, fetch and return the result of the query (default is False).
        :return: Result of the query if fetch_result is True, otherwise None.

        Example:
        >> custom_query = "SELECT * FROM your_table WHERE age > $1"
        >> query_params = (25,)
        >> result = await crud_instance.execute_query(custom_query, query_params, fetch_result=True)
        >> print(result)
        """
        if not unsafe:
            self._check_query_safety(query, params)

        async with self._get_connection_cursor() as connection:
            prepared_params = tuple(params) if params else None
            if fetch_result:
                result = (
                    await connection.fetch(query, *prepared_params)
                    if prepared_params
                    else await connection.fetch(query)
                )
            else:
                result = None
                await connection.execute(
                    query, *prepared_params
                ) if prepared_params else await connection.execute(query)

            return result

    @staticmethod
    def _check_query_safety(query: str, params: Union[None, tuple] = None):
        """
        Check if the query is safe by examining the query string and parameters.

        :param query: SQL query string with placeholders for parameters.
        :param params: Tuple of parameters for the query (default is None).
        :raises CustomQueryError: If the query is considered unsafe.
        """

        unsafe_keywords = ["DELETE", "DROP", "TRUNCATE", "ALTER"]

        if any(keyword in query.upper() for keyword in unsafe_keywords):
            raise UnsafeCRUDError(query, params)

        if params:
            # Additional checks based on the parameters can be added if needed.
            pass
