import sqlite3
import traceback


def sqlite_write(db_uri, schema, variable_name, variable_value, request_id):
    """
    The function writes a variable value to a SQLite database using the provided database URI, schema,
    variable name, variable value, and request ID.

    :param db_uri: The URI or path to the SQLite database file
    :param schema: The schema parameter refers to the name of the table or schema in the database where
    you want to write the data
    :param variable_name: The name of the variable you want to write to the SQLite database
    :param variable_value: The value of the variable that you want to write to the SQLite database
    :param request_id: The unique identifier for the request being made. It can be used to track and
    identify the specific request in the database
    """
    try:
        conn = sqlite3.connect(db_uri)
        cursor = conn.cursor()

        # Get table name and fields from schema dictionary
        table_name = schema["name"]
        fields = schema["fields"]

        # Create table if not exists
        field_definitions = (
            "unique_id INTEGER PRIMARY KEY AUTOINCREMENT, request_id TEXT, "
        )
        field_definitions += ", ".join(
            [f"{field} {data_type}" for field, data_type in fields.items()]
        )
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions})")

        # Create placeholders for the field values
        placeholders = ", ".join(["?" for _ in fields])

        # Insert a new record
        field_names = ", ".join(fields.keys())

        field_values = [request_id, variable_name, variable_value]
        cursor.execute(
            f"INSERT INTO {table_name} (request_id, {field_names}) VALUES (?, {placeholders})",
            field_values,
        )

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(traceback.print_exc())
        return False


def create_sqlite_table(db_uri, schema_map):
    """
    Create a SQLite table based on the provided schema map.

    Args:
        db_uri (str): The URI of the SQLite database.
        schema_map (dict): A dictionary containing the schema information for the table.

    Returns:
        bool: True if the table is created successfully, False otherwise.
    """
    try:
        # Connect to database
        conn = sqlite3.connect(db_uri)
        cursor = conn.cursor()

        # Get table name and fields from schema map
        table_name = schema_map["name"]
        fields = schema_map["fields"]

        # Create field definitions (e.g. "unique_id INTEGER PRIMARY KEY AUTOINCREMENT, request_id TEXT, field1 DATATYPE, field2 DATATYPE, ...")
        field_definitions = (
            "unique_id INTEGER PRIMARY KEY AUTOINCREMENT, request_id TEXT, "
            + ", ".join([f"{field} {data_type}" for field, data_type in fields.items()])
        )

        # Create table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions})")

        # Commit and close connection
        conn.commit()
        conn.close()
        return True

    # Except if connection fails
    except Exception as e:
        print(traceback.print_exc())

    return False
