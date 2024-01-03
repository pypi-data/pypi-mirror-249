from __future__ import annotations

import random
from contextlib import contextmanager
from typing import Optional, Dict, List, Union

from psycopg import connect, sql
from psycopg.rows import dict_row


class PsycoPGCRUD:
    def __init__(
        self,
        connection_params: Dict[str, Union[str, int]],
        table_name: str,
        columns: Dict[str, str],
        binary: bool = False,
    ):
        """
        Initialize PostgreSQLCRUD instance.

        :param connection_params: Dictionary containing PostgreSQL connection parameters.
        :param table_name: Name of the database table.
        :param columns: Dictionary containing column names and their data types.
        :param binary: If True, set the client encoding to 'utf-8'.

        Example::

        >> connection_params = {"host": "your_host", "database": "your_database", "user": "your_user",
        >> "password": "your_password"}
        >> table_name = "your_table"
        >> columns = {"id": "serial", "name": "varchar(255)", "age": "int"}
        >> crud_instance = PostgreSQLCRUD(connection_params, table_name, columns)
        """
        self.connection_params = connection_params
        if not binary:
            self.connection_params["client_encoding"] = "utf-8"
        self.table_name = table_name
        self.columns = columns

    @contextmanager
    def _get_connection_cursor(self):
        """
        Context manager for obtaining a database connection cursor.

        :yield: Database cursor.

        Example:
        >> with crud_instance._get_connection_cursor() as cursor:
        ...     cursor.execute("SELECT * FROM your_table")
        ...     result = cursor.fetchall()
        ...     print(result)
        """
        connection = connect(**self.connection_params, row_factory=dict_row)
        connection.autocommit = True
        cursor = connection.cursor(row_factory=dict_row)
        # cursor.execute("SET client_encoding TO 'utf8'")
        try:
            yield cursor
        finally:
            cursor.close()
            connection.close()

    def create_table(self):
        """
        Create a table in the database.

        If the table already exists, it does nothing.

        :return: None

        Example:
        >> crud_instance.create_table()
        """
        create_table_query = sql.SQL(
            "CREATE TABLE IF NOT EXISTS {table} ({columns})"
        ).format(
            table=sql.Identifier(self.table_name),
            columns=sql.SQL(", ").join(
                sql.SQL("{column} {data_type}").format(
                    column=sql.Identifier(column), data_type=sql.SQL(data_type)  # type: ignore
                )
                for column, data_type in self.columns.items()
            ),
        )

        with self._get_connection_cursor() as cursor:
            cursor.execute(create_table_query)

    def _build_insert_query(self, data: Dict[str, Union[str, int]]):
        """
        Build SQL INSERT query.

        :param data: Dictionary containing column-value pairs to be inserted.
        :return: SQL query.

        Example:
        >> data = {"name": "John Doe", "age": 30}
        >> insert_query = crud_instance._build_insert_query(data)
        >> with crud_instance._get_connection_cursor() as cursor:
        ...     cursor.execute(insert_query, tuple(data.values()))
        """
        columns = data.keys()
        values = data.values()
        return sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
            table=sql.Identifier(self.table_name),
            columns=sql.SQL(", ").join(map(sql.Identifier, columns)),
            values=sql.SQL(", ").join(sql.Placeholder() for _ in values),
        )

    def create(self, data: Dict[str, Union[str, int]]):
        """
        Insert a record into the database.

        :param data: Dictionary containing column-value pairs.
        :return: None

        Example:
        >> data = {"name": "John Doe", "age": 30}
        >> crud_instance.create(data)
        """
        insert_query = self._build_insert_query(data)
        with self._get_connection_cursor() as cursor:
            cursor.execute(insert_query, tuple(data.values()))

    def _build_select_query(
        self,
        conditions: Optional[Dict[str, Union[str, int]]] = None,
        columns_clause: sql.SQL | sql.Composed = sql.SQL("*"),
    ) -> sql.SQL | sql.Composed:
        """
        Build SQL SELECT query.

        :param conditions: Dictionary containing column-value pairs for WHERE clause.
        :param columns_clause: SQL | Composed fragment for the columns to be selected.
        :return: SQL | Composed query.

        Example:
        >> conditions = {"age": 25}
        >> columns_to_select = ["name", "age"]
        >> select_query = crud_instance._build_select_query(conditions, columns_to_select)
        >> with crud_instance._get_connection_cursor() as cursor:
        ...     cursor.execute(select_query, tuple(conditions.values()))
        ...     result = cursor.fetchall()
        ...     print(result)
        """
        where_conditions = (
            sql.SQL(" WHERE ")
            + sql.SQL(" AND ").join(
                sql.SQL("{key} = %s").format(key=sql.Identifier(key))
                for key in conditions.keys()
            )
            if conditions
            else sql.SQL("")
        )

        return sql.SQL("SELECT {columns} FROM {table}{where_conditions}").format(
            columns=columns_clause,
            table=sql.Identifier(self.table_name),
            where_conditions=where_conditions,
        )

    def read_all(self):
        """
        Read all records from the database.

        :return: List of dictionaries representing database records.

        Example:
        >> all_records = crud_instance.read_all()
        >> print(all_records)
        """
        select_query = self._build_select_query()
        with self._get_connection_cursor() as cursor:
            cursor.execute(select_query)
            return cursor.fetchall()

    def read(self, conditions: Dict[str, Union[str, int]]):
        """
        Read a record from the database based on conditions.

        :param conditions: Dictionary containing column-value pairs for WHERE clause.
        :return: Dictionary representing a database record.

        Example:
        >> conditions = {"name": "John Doe"}
        >> record = crud_instance.read(conditions)
        >> print(record)
        """
        select_query = self._build_select_query(conditions)
        with self._get_connection_cursor() as cursor:
            cursor.execute(select_query, tuple(conditions.values()))
            return cursor.fetchone()

    def read_columns(
        self,
        conditions: Dict[str, Union[str, int]],
        columns: Optional[List[str]] = None,
    ):
        """
        Read specific columns of a record from the database based on conditions.

        :param conditions: Dictionary containing column-value pairs for WHERE clause.
        :param columns: List of column names to be selected.
        :return: Dictionary representing a database record with specified columns.

        Example:
        >> conditions = {"name": "John Doe"}
        >> columns_to_select = ["name", "age"]
        >> record = crud_instance.read_columns(conditions, columns_to_select)
        >> print(record)
        """
        if not columns:
            # If columns are not specified, select all columns
            columns_clause = sql.SQL("*")
        else:
            # Use specified columns in the SELECT statement
            columns_clause = sql.SQL(", ").join(map(sql.Identifier, columns))  # type: ignore

        select_query = self._build_select_query(conditions, columns_clause)
        with self._get_connection_cursor() as cursor:
            cursor.execute(select_query, tuple(conditions.values()))
            return cursor.fetchone()

    def _build_update_query(
        self,
        data: Dict[str, Union[str, int]],
        conditions: Dict[str, Union[str, int]],
    ):
        """
        Build SQL UPDATE query.

        :param data: Dictionary containing column-value pairs to be updated.
        :param conditions: Dictionary containing column-value pairs for WHERE clause.
        :return: SQL query.

        Example:
        >> update_data = {"age": 31}
        >> update_conditions = {"name": "John Doe"}
        >> update_query = crud_instance._build_update_query(update_data, update_conditions)
        >> with crud_instance._get_connection_cursor() as cursor:
        ...     cursor.execute(update_query, tuple(update_data.values()) + tuple(update_conditions.values()))
        """
        set_clause = sql.SQL(", ").join(
            sql.SQL("{key} = %s").format(key=sql.Identifier(key)) for key in data.keys()
        )
        where_conditions = sql.SQL(" AND ").join(
            sql.SQL("{key} = %s").format(key=sql.Identifier(key))
            for key in conditions.keys()
        )
        return sql.SQL(
            "UPDATE {table} SET {set_clause} WHERE {where_conditions}"
        ).format(
            table=sql.Identifier(self.table_name),
            set_clause=set_clause,
            where_conditions=where_conditions,
        )

    def update(
        self,
        data: Dict[str, Union[str, int]],
        conditions: Dict[str, Union[str, int]],
    ):
        """
        Update records in the database based on conditions.

        :param data: Dictionary containing column-value pairs to be updated.
        :param conditions: Dictionary containing column-value pairs for WHERE clause.
        :return: None

        Example:
        >> update_data = {"age": 31}
        >> update_conditions = {"name": "John Doe"}
        >> crud_instance.update(update_data, update_conditions)
        """
        update_query = self._build_update_query(data, conditions)
        with self._get_connection_cursor() as cursor:
            cursor.execute(
                update_query, tuple(data.values()) + tuple(conditions.values())
            )

    def _build_delete_query(self, conditions: Dict[str, Union[str, int]]):
        """
        Build SQL DELETE query.

        :param conditions: Dictionary containing column-value pairs for WHERE clause.
        :return: SQL query.

        Example:
        >> delete_conditions = {"name": "John Doe"}
        >> delete_query = crud_instance._build_delete_query(delete_conditions)
        >> with crud_instance._get_connection_cursor() as cursor:
        ...     cursor.execute(delete_query, tuple(delete_conditions.values()))
        """
        where_conditions = sql.SQL(" AND ").join(
            sql.SQL("{key} = %s").format(key=sql.Identifier(key))
            for key in conditions.keys()
        )
        return sql.SQL("DELETE FROM {table} WHERE {where_conditions}").format(
            table=sql.Identifier(self.table_name),
            where_conditions=where_conditions,
        )

    def delete(self, conditions: Dict[str, Union[str, int]]):
        """
        Delete records from the database based on conditions.

        :param conditions: Dictionary containing column-value pairs for WHERE clause.
        :return: None

        Example:
        >> delete_conditions = {"name": "John Doe"}
        >> crud_instance.delete(delete_conditions)
        """
        delete_query = self._build_delete_query(conditions)
        with self._get_connection_cursor() as cursor:
            cursor.execute(delete_query, tuple(conditions.values()))

    def get_random_item(self):
        """
        Get a random record from the database.

        :return: Dictionary representing a random database record.

        Example:
        >> random_record = crud_instance.get_random_item()
        >> print(random_record)
        """
        count_query = sql.SQL("SELECT COUNT(*) FROM {table}").format(
            table=sql.Identifier(self.table_name)
        )

        with self._get_connection_cursor() as cursor:
            cursor.execute(count_query)
            total_rows = cursor.fetchone()

            if len(total_rows) > 0:
                random_offset = random.randint(0, len(total_rows) - 1)
                select_query = sql.SQL(
                    "SELECT * FROM {table} OFFSET %s LIMIT 1"
                ).format(table=sql.Identifier(self.table_name))
                cursor.execute(select_query, (random_offset,))
                return cursor.fetchone()
            else:
                return None

    def execute_query(
        self,
        query: str,
        params: Union[None, tuple] = None,
        fetch_result: bool = False,
    ):
        """
        Execute a custom SQL query using prepared statements.

        :param query: SQL query string with placeholders for parameters.
        :param params: Tuple of parameters for the query (default is None).
        :param fetch_result: If True, fetch and return the result of the query (default is False).
        :return: Result of the query if fetch_result is True, otherwise None.

        Example:
        >> custom_query = "SELECT * FROM your_table WHERE age > %s"
        >> query_params = (25,)
        >> result = crud_instance.execute_query(custom_query, query_params, fetch_result=True)
        >> print(result)
        """
        with self._get_connection_cursor() as cursor:
            cursor.execute(query, params)

            if fetch_result:
                result = cursor.fetchall()
                return result
