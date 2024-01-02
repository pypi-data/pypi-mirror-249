### Database Modules:

1. [AsyncPG CRUD Module](#asyncpg-crud-module)
    - [AsyncPG CRUD Class](#asyncpg-crud-class)
        - [Parameters](#parameters-idasyncpg-parameters)
        - [Methods](#methods-idmethods_asyncpg)
        - [Examples](#examples-idexamples_asyncpg)

2. [PsycoPG CRUD Module](#psycopg-crud-module)
    - [PsycoPG CRUD Class](#psycopgcrud-class)
        - [Parameters](#parameters-idparamaters-psycopg)
        - [Methods](#methods-idmethods-psycopg)
        - [Examples](#examples-idexamples-psycopg)

### Logging Modules:

1. [Log File Parser Module](#log-file-parser-module)
    - [LogEntry NamedTuple](#logentry-namedtuple-idlogentry-namedtuple)
    - [LogFileParser Class](#logfileparser-class-idlogfile-parser-class)
        - [Parameters](#parameters-idlog_parser_parameters)
        - [Methods](#methods-idlogfile-parser-methods)
        - [Examples](#examples-idlogfile-parser-examples)

2. [Timed Rotating Log Module](#timed-rotating-log-module)
    - [Usage](#usage-idusage_timed_rotating_log)
        - [Initialization](#initialization-idinitialization_timed_rotating_log)
        - [Logging Methods](#logging-methods-idmethods_times_rotating_log)
        - [Parameters](#parameters-idparameters_timed_rotating_log)
        - [Log Rotation](#log-rotation-idrotation_timed_rotating_log)
        - [Customization](#customization-idcustomization_timed_rotating_log)

3. [Rotating Log Module](#rotating-log-module)
    - [Usage](#usage-idusage_rotating_log)
        - [Parameters](#parameters-idparameters_rotating_log)
        - [Log Rotation](#log-rotation-idlogrotation_rotating_log)
        - [Customization](#customization-idcustomization_rotating_log)

### Configuration Modules:

1. [YAML Configuration Module](#yaml-configuration-module-idyaml_module)
    - [YAMLConfigDict Class](#yamlconfigdict-class)
        - [Parameters](#parameters-idparameters_yaml_config_dict)
        - [Example Usage](#example-usage-idexample-usage_yaml_config_dict)
    - [YAMLConfig Class](#yamlconfig-class)
        - [Parameters](#parameters-idparameters_yaml_config)
        - [Example Usage](#example-usage-idexample_usage_yaml_config)
        - [Dependencies](#dependencies-iddependencies_yaml)

2. [XML Configuration Module](#xml-configuration-module-idxml_module)
    - [XMLConfig Class](#xmlconfig-class)
        - [Parameters](#parameters-idparameters_xml_config)
        - [Class Methods](#class-methods-idclass_methods_xml)
        - [Example Usage](#example-usage-idexample-usage_xml)
        - [Dependencies](#dependencies-iddependencies_xml)

3. [TOML Configuration Module](#toml-configuration-module-idtoml_module)
    - [TOMLConfigDict Class](#tomlconfigdict-class)
        - [Parameters](#parameters-idparameters_toml_config_dict)
        - [Example Usage](#example-usage-idexample-usage_toml_config_dict)
    - [TOMLConfig Class](#tomlconfig-class)
        - [Parameters](#parameters-idparameters_toml_config)
        - [Example Usage](#example-usage-idexample_usage_toml_dict)
        - [Dependencies](#dependencies-iddependencies_toml)

4. [Properties Configuration Module](#properties-configuration-module-idproperties_module)
    - [PropertiesConfigDict Class](#propertiesconfigdict-class)
        - [Parameters](#parameters-idparameters_properties_config_dict)
        - [Example Usage](#example-usage-idexample-usage_properties_config_dict)
    - [PropertiesConfig Class](#propertiesconfig-class)
        - [Parameters](#parameters-idparameters_properties_config)
        - [Example Usage](#example-usage-idexample_usage_properties_config)
        - [Dependencies](#dependencies-iddependencies_properties)

5. [JSON Configuration Module](#json-configuration-module-idjson_module)
    - [JSONConfigDict Class](#jsonconfigdict-class)
        - [Parameters](#parameters-idparameters_json_config_dict)
        - [Example Usage](#example-usage-idexample-usage_json_config_dict)
    - [JSONConfig Class](#jsonconfig-class)
        - [Parameters](#parameters-idparameters_json_config)
        - [Example Usage](#example-usage-idexample_usage_json_config)
        - [Dependencies](#dependencies-iddependencies_json)

# Database Modules

## AsyncPG CRUD Module:

### AsyncPG CRUD Class

#### Parameters {id="asyncpg-parameters"}

- `connection_params`: A dictionary containing connection parameters for the PostgreSQL database.
    - Type: `dict`
- `table_name`: The name of the table in the database.
    - Type: `str`
- `columns`: A dictionary representing the columns of the table along with their data types.
    - Type: `dict`

#### Methods {id="methods_asyncpg"}

##### `create_table() -> None`  {id="create-table-asyncpg"}

Creates the table in the database if it does not exist.

##### `create(data: dict) -> None`

Inserts a new row into the table with the provided data.

##### `read_all() -> List[asyncpg.Record]`

Fetches all rows from the table.

##### `read(conditions: dict) -> Optional[asyncpg.Record]`

Fetches a single row from the table based on the provided conditions.

##### `read_columns(conditions: dict, columns: list = None) -> Optional[asyncpg.Record]`

Fetches specific columns from a single row based on the provided conditions.

##### `update(data: dict, conditions: dict) -> None`

Updates rows in the table based on the provided conditions with the new data.

##### `delete(conditions: dict) -> None`

Deletes rows from the table based on the provided conditions.

##### `get_random_item() -> Optional[asyncpg.Record]`

Fetches a random row from the table.

##### `execute_query(query: str, params: Optional[list] = None, fetch_result: bool = False) -> Optional[asyncpg.Record]`

Executes a custom SQL query on the database.

### Examples {id="examples_asyncpg"}

```python
from unitstools import AsyncPGCRUD

# Create an instance of AsyncPGCRUD
crud_instance = AsyncPGCRUD(
    connection_params={
        "database": "your_database",
        "user": "your_user",
        "password": "your_password",
        "host": "your_host",
        "port": "your_port",
    },
    table_name="your_table",
    columns={"column1": "data_type1", "column2": "data_type2"},
)

# Create the table
await crud_instance.create_table()

# Insert data into the table
await crud_instance.create({"column1": value1, "column2": value2})

# Fetch all rows from the table
all_rows = await crud_instance.read_all()

# Fetch a specific row based on conditions
specific_row = await crud_instance.read({"column1": value1})

# Update rows in the table
await crud_instance.update({"column1": new_value}, {"column2": value2})

# Delete rows from the table
await crud_instance.delete({"column1": value1})

# Fetch a random item from the table
random_item = await crud_instance.get_random_item()

# Execute a custom query
custom_query_result = await crud_instance.execute_query("SELECT * FROM your_table WHERE column1 = $1", [value1],
                                                        fetch_result=True, unsafe=An)
```

## PsycoPG CRUD Module:

### PsycoPGCRUD Class

#### Parameters {id="paramaters-psycopg"}

- `connection_params`: A dictionary containing PostgreSQL connection parameters.
    - Type: `Dict[str, Union[str, int]]`
- `table_name`: The name of the database table.
    - Type: `str`
- `columns`: A dictionary containing column names and their data types.
    - Type: `Dict[str, str]`
- `binary`: If True, set the client encoding to 'utf-8'.
    - Type: `bool`, Default: `False`

#### Methods {id="methods-psycopg"}

##### `create_table() -> None`

Creates a table in the database if it does not exist.

##### `create(data: Dict[str, Union[str, int]]) -> None`

Inserts a new record into the table with the provided data.

##### `read_all() -> List[Dict[str, Union[str, int]]]`

Fetches all records from the table.

##### `read(conditions: Dict[str, Union[str, int]]) -> Optional[Dict[str, Union[str, int]]]`

Fetches a single record from the table based on the provided conditions.

##### `read_columns(conditions: Dict[str, Union[str, int]], columns: List[str] = None) -> Optional[Dict[str, Union[str, int]]]`

Fetches specific columns from a single record based on the provided conditions.

##### `update(data: Dict[str, Union[str, int]], conditions: Dict[str, Union[str, int]]) -> None`

Updates records in the table based on the provided conditions with the new data.

##### `delete(conditions: Dict[str, Union[str, int]]) -> None`

Deletes records from the table based on the provided conditions.

##### `get_random_item() -> Optional[Dict[str, Union[str, int]]]`

Fetches a random record from the table.

##### `execute_query(query: str, params: Optional[Tuple] = None, fetch_result: bool = False) -> Optional[List[Dict[str, Union[str, int]]]]`

Executes a custom SQL query on the database.

### Examples {id="examples-psycopg"}

```python
from unitstools import PsycoPGCRUD

# Create an instance of PsycoPGCRUD
crud_instance = PsycoPGCRUD(
    connection_params={
        "host": "your_host",
        "database": "your_database",
        "user": "your_user",
        "password": "your_password"
                    "client_encoding": "utf-8"
},
table_name = "your_table",
columns = {"id": "serial", "name": "varchar(255)", "age": "int"}
)

# Create the table
crud_instance.create_table()

# Insert data into the table
data = {"name": "John Doe", "age": 30}
crud_instance.create(data)

# Fetch all records from the table
all_records = crud_instance.read_all()

# Fetch a specific record based on conditions
conditions = {"name": "John Doe"}
specific_record = crud_instance.read(conditions)

# Fetch specific columns of a record based on conditions
columns_to_select = ["name", "age"]
record_with_columns = crud_instance.read_columns(conditions, columns_to_select)

# Update records in the table
update_data = {"age": 31}
update_conditions = {"name": "John Doe"}
crud_instance.update(update_data, update_conditions)

# Delete records from the table
delete_conditions = {"name": "John Doe"}
crud_instance.delete(delete_conditions)

# Fetch a random item from the table
random_item = crud_instance.get_random_item()

# Execute a custom query
custom_query = "SELECT * FROM your_table WHERE age > %s"
query_params = (25,)
result = crud_instance.execute_query(custom_query, query_params, fetch_result=True, unsafe=An)
```

# Logging Modules

## Log File Parser Module

### LogEntry NamedTuple {id="logentry-namedtuple"}

Represents a log entry with timestamp, log level, filename, line number, and log message.

```python 
class LogEntry(NamedTuple):
    timestamp: datetime
    level: str
    filename: str
    lineno: int
    message: str
```

#### Fields {id="logfile-parser-fields"}

- `timestamp`: Datetime object representing the timestamp of the log entry.
    - Type: `datetime`
- `level`: Log level of the entry.
    - Type: `str`
- `filename`: Filename where the log entry originated.
    - Type: `str`
- `lineno`: Line number in the file where the log entry occurred.
    - Type: `int`
- `message`: Log message.
    - Type: `str`

### LogFileParser Class {id="logfile-parser-class"}

Parses log files with a specified format and extracts log entries.

#### Parameters {id="log_parser_parameters"}

- `log_format`: Regular expression pattern for parsing log lines.
    - Type: `str`

#### Methods {id="logfile-parser-methods"}

##### `__init__(log_format: str = None) -> None`

Initializes a LogFileParser with the specified log format.

##### `parse_log_line(log_line: str, force: bool = False) -> Optional[LogEntry]`

Parses a single log line and returns a LogEntry if successful.

- Parameters:
    - `log_line`: Log line to be parsed.
        - Type: `str`
    - `force`: If True, creates a LogEntry even for unparsable lines.
        - Type: `bool`
- Returns:
    - Parsed LogEntry or None.
        - Type: `Optional[LogEntry]`

##### `parse_log_file(log_file_path: str, force: bool = False) -> List[LogEntry]`

Parses a log file and returns a list of LogEntry objects.

- Parameters:
    - `log_file_path`: Path to the log file.
        - Type: `str`
    - `force`: If True, includes entries for unparsable lines.
        - Type: `bool`
- Returns:
    - List of LogEntry objects.
        - Type: `List[LogEntry]`

### Examples {id="logfile-parser-examples"}

```python
from unitstools import LogFileParser

# Create an instance of LogFileParser
log_parser = LogFileParser(log_format=r'\[(?P<timestamp>.*?)\] '
                                      r'(?P<level>\w+) '
                                      r'\[(?P<filename>.*?):(?P<lineno>\d+)\] '
                                      r'(?P<message>.*)')

# Parse a single log line
log_line = "[2023-01-01 12:00:00] INFO [example.py:10] Log message"
parsed_entry = log_parser.parse_log_line(log_line)
print(parsed_entry)

# Parse a log file
log_file_path = "path/to/your/logfile.log"
log_entries = log_parser.parse_log_file(log_file_path)
print(log_entries)
```

## Timed Rotating Log Module

The `TimedRotatingLog` is a Python class that facilitates logging with a TimedRotatingFileHandler for automatic log file
rotation. This is particularly useful for managing log files over time to prevent them from becoming too large.

### Usage {id="usage_timed_rotating_log"}

#### Initialization {id="initialization_timed_rotating_log"}

To use the `TimedRotatingLog` class, instantiate it with the following parameters:

- `name` (str): The name of the logger.
- `level` (int | Level): The log level (default is `Level.INFO`).
- `path` (str): The path where the log file will be created (default is the current working directory).
- `timer` (int): The interval for rotating log files in minutes (default is 1440, equivalent to 24 hours).
- `max_backups` (int): Maximum number of backups before old files are overwritten (default is 14).
- `log_format` (str): The format string for log messages (default is a standard format).

#### Logging Methods {id="methods_times_rotating_log"}

The `TimedRotatingLog` class provides the following logging methods:

- `info(message: str)`: Writes a log message with the INFO level.
- `warn(message: str)`: Writes a log message with the WARNING level.
- `error(message: str)`: Writes a log message with the ERROR level.
- `debug(message: str)`: Writes a log message with the DEBUG level.
- `critical(message: str)`: Writes a log message with the CRITICAL level.

#### Example {id="example_timed_rotating_log"}

```python
from my_logging_module import TimedRotatingLog, Level

# Instantiate the logger
logger = TimedRotatingLog(name="MyLogger", level=Level.DEBUG, path="/path/to/logs")

# Log some messages
logger.info("This is an informational message.")
logger.error("An error occurred!")

# Customize log format
custom_logger = TimedRotatingLog(name="CustomLogger", log_format="[%(levelname)s] %(message)s")

# Log with the custom format
custom_logger.warn("Custom warning message.")
```

### Parameters {id="parameters_timed_rotating_log"}

- `name`: The name of the logger.
- `level`: The log level (use the `Level` enumeration or an integer).
- `path`: The path where the log file will be created.
- `timer`: The interval for rotating log files in minutes.
- `max_backups`: Maximum number of backups before old files are overwritten.
- `log_format`: The format string for log messages.

### Log Rotation {id="rotation_timed_rotating_log"}

The log files are rotated based on the specified time interval (`timer`). Old log files are retained up to the maximum
number of backups (`max_backups`). The log files are named with a timestamp suffix for easy identification.

### Customization {id="customization_timed_rotating_log"}

You can customize the log format by providing your own format string when instantiating the logger. Additionally, you
can configure the log level and path according to your requirements.

## Rotating Log Module

The `RotatingLog` is a Python class designed for logging with a `RotatingFileHandler` that enables log file rotation
based on size. This is useful to prevent log files from growing too large and consuming excessive disk space.

### Usage {id="usage_rotating_log"}

#### Initialization: {id="initalization_rotating_log"}

To use the `RotatingLog` class, instantiate it with the following parameters:

- `name` (str): The name of the logger.
- `level` (int | Level): The log level (default is `Level.INFO`).
- `path` (str): The path where the log file will be created (default is the current working directory).
- `max_size` (int): Maximum logfile size in megabytes before rotating files (default is 32 MB).
- `max_backups` (int): Maximum number of backups before old files are overwritten (default is 14).
- `log_format` (str): The format string for log messages (default is a standard format).

#### Logging Methods: {id="methods_rotating_log"}

The `RotatingLog` class provides the following logging methods:

- `info(message: str)`: Writes a log message with the INFO level.
- `warn(message: str)`: Writes a log message with the WARNING level.
- `error(message: str)`: Writes a log message with the ERROR level.
- `debug(message: str)`: Writes a log message with the DEBUG level.
- `critical(message: str)`: Writes a log message with the CRITICAL level.

#### Example: {id="examples_rotating_log"}

```python
from my_logging_module import RotatingLog, Level

# Instantiate the logger
logger = RotatingLog(name="MyLogger", level=Level.DEBUG, path="/path/to/logs")

# Log some messages
logger.info("This is an informational message.")
logger.error("An error occurred!")

# Customize log format
custom_logger = RotatingLog(name="CustomLogger", log_format="[%(levelname)s] %(message)s")

# Log with the custom format
custom_logger.warn("Custom warning message.")
```

### Parameters: {id="parameters_rotating_log"}

- `name`: The name of the logger.
- `level`: The log level (use the `Level` enumeration or an integer).
- `path`: The path where the log file will be created.
- `max_size`: Maximum logfile size before rotating files.
- `max_backups`: Maximum number of backups before old files are overwritten.
- `log_format`: The format string for log messages.

### Log Rotation: {id="logrotation_rotating_log"}

Log files are rotated based on the specified maximum size (`max_size`). Old log files are retained up to the maximum
number of backups (`max_backups`).

### Customization {id="customization_rotating_log"}

You can customize the log format by providing your own format string when instantiating the logger. Additionally, you
can configure the log level, path, maximum size, and maximum number of backups according to your requirements.

# Configuration Modules

## YAML Configuration Module {id="yaml_module"}

### YAMLConfigDict Class

#### Parameters {id="parameters_yaml_config_dict"}

- `config_dict`: The input configuration dictionary.
    - Type: `dict`
- `depth`: The depth to which the conversion should occur. Default is 5.
    - Type: `int`

#### Example Usage {id="example-usage_yaml_config_dict}

```python
from unitstools import YAMLConfigDict

# Beispielcode hier

config_dict = YAMLConfigDict(param1=value1, param2=value2)
```

### YAMLConfig Class

#### Parameters {id="parameters_yaml_config"}

- `filepath`: The path to the YAML configuration file.
    - Type: `Path`
- `depth`: The depth to which the conversion should occur. Default is 5.
    - Type: `int`

#### Example Usage {id="example_usage_yaml_config"}

```python
from unitstools import YAMLConfig

# Beispielcode hier

config = YAMLConfig(filepath=path_to_yaml_file, depth=5)
```

### Dependencies {id="dependencies_yaml"}

- `re`: Regular expression module.
- `pathlib.Path`: Path module for handling file paths.
- `yaml`: YAML parsing module.

## XML Configuration Module {id="xml_module"}

### XMLConfig Class

#### Parameters {id="parameters_xml_config"}

- `filepath`: The path to the XML configuration file.
    - Type: `Path`
- `depth`: The depth to which the parsing should occur. Default is 10.
    - Type: `int`

#### Class Methods {id="class_methods_xml"}

##### `parse_from_xml_string(xml_string: str, depth: int = 10) -> XMLConfig`

Parses an XML string and creates an XMLConfig object.

- `xml_string`: The XML string to parse.
    - Type: `str`
- `depth`: The depth to which the parsing should occur. Default is 10.
    - Type: `int`

#### Example Usage {id="example-usage_xml"}

```python
from unitstools import XMLConfig

# Beispielcode hier

xml_string = "<root><element1>value1</element1><element2>value2</element2></root>"
config = XMLConfig.parse_from_xml_string(xml_string, depth=5)
```

#### Example Usage {id="example-usage_xml_2"}

```python
from unitstools import XMLConfig

# Beispielcode hier

config = XMLConfig(filepath=path_to_xml_file, depth=5)
```

#### Dependencies {id="dependencies_xml"}

- `collections.namedtuple`: Named tuple for representing XML structure.
- `pathlib.Path`: Path module for handling file paths.
- `xml.etree.ElementTree`: ElementTree module for XML parsing.

## TOML Configuration Module {id="toml_module"}

### TOMLConfigDict Class

#### Parameters {id="parameters_toml_config_dict"}

- `config_dict`: The input configuration dictionary.
    - Type: `dict`

- `depth`: The depth to which the conversion should occur. Default is 5.
    - Type: `int`

#### Example Usage {id="example-usage_toml_config_dict"}

```python
from unitstools import TOMLConfigDict

# Beispielcode hier

config_dict = TOMLConfigDict(param1=value1, param2=value2)
```

### TOMLConfig Class

#### Parameters {id="parameters_toml_config"}

- `filepath`: The path to the TOML configuration file.
    - Type: `Path`

- `depth`: The depth to which the conversion should occur. Default is 5.
    - Type: `int`

#### Example Usage {id="example_usage_toml_dict"}

```python
from unitstools import TOMLConfig

# Beispielcode hier

config = TOMLConfig(filepath=path_to_config_file, depth=5)
```

#### Dependencies {id="dependencies_toml"}

- `re`: Regular expression module.
- `pathlib.Path`: Path module for handling file paths.
- `toml`: TOML file parsing module.

## Properties Configuration Module {id="properties_module"}

### PropertiesConfigDict Class

#### Parameters {id="parameters_properties_config_dict"}

- `config_dict`: The dictionary to convert to a ConfigDict.
    - Type: `dict`
- `depth`: The depth limit for nested configurations. Default is 5.
    - Type: `int`

#### Example Usage {id="example-usage_properties_config_dict"}

```python
from unitstools import PropertiesConfigDict

# Beispielcode hier

config_dict = PropertiesConfigDict(param1=value1, param2=value2)
```

### PropertiesConfig Class

#### Parameters {id="parameters_properties_config"}

- `filepath`: The path to the properties configuration file.
    - Type: `Path`
- `depth`: The depth limit for nested configurations. Default is 5.
    - Type: `int`

#### Example Usage {id="example_usage_properties_config"}

```python
from unitstools import PropertiesConfig

# Beispielcode hier

config = PropertiesConfig(filepath=path_to_properties_file, depth=5)
```

#### Dependencies {id="dependencies_properties"}

- `re`: Regular expression module.
- `pathlib.Path`: Path module for handling file paths.

## JSON Configuration Module {id="json_module"}

### JSONConfigDict Class

#### Parameters {id="parameters_json_config_dict"}

- `config_dict`: The input configuration dictionary.
    - Type: `dict`
- `depth`: The depth to which the conversion should occur. Default is 5.
    - Type: `int`

#### Example Usage {id="example-usage_json_config_dict"}

```python
from unitstools import JSONConfigDict

# Beispielcode hier

config_dict = JSONConfigDict(param1=value1, param2=value2)
```

### JSONConfig Class

#### Parameters {id="parameters_json_config"}

- `filepath`: The path to the JSON configuration file.
    - Type: `Path`
- `depth`: The depth to which the conversion should occur. Default is 5.
    - Type: `int`

#### Example Usage {id="example_usage_json_config"}

```python
from unitstools import JSONConfig

# Beispielcode hier

config = JSONConfig(filepath=path_to_json_file, depth=5)
```

#### Dependencies {id="dependencies_json"}

- `re`: Regular expression module.
- `pathlib.Path`: Path module for handling file paths.
- `json`: JSON parsing module.