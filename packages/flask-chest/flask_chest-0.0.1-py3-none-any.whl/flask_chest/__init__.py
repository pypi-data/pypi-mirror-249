import json
import traceback

from flask import Flask

from .sqlite_utils import create_sqlite_table, sqlite_write

DEFAULT_SCHEMA = {
    "name": "flask_chest",
    "fields": {
        "name": "TEXT",
        "value": "TEXT",
    },
}


class FlaskChest:
    """
    Flask extension for storing and retrieving key-value pairs in a SQLite database.

    Args:
        app (Flask): The Flask application instance.

    Attributes:
        app (Flask): The Flask application instance.

    """

    def __init__(self, app: Flask):
        self.app = app

        # Register extension with app
        if not hasattr(app, "extensions"):
            app.extensions = {}

        app.extensions["flask_chest"] = self


class FlaskChestSQLite(FlaskChest):
    """
    Flask extension for storing and retrieving key-value pairs in a SQLite database.

    Args:
        app (Flask): The Flask application instance.
        name (str, optional): The name of the SQLite table. Defaults to "flask_chest".
        db_uri (str, optional): The URI of the SQLite database. Defaults to "db.sqlite3".

    Attributes:
        app (Flask): The Flask application instance.
        db_uri (str): The URI of the SQLite database.

    """

    def __init__(
        self, app: Flask, name: str = "flask_chest", db_uri: str = "db.sqlite3"
    ):
        super().__init__(app)
        self.db_uri = db_uri  # Database URI
        self.register_table(name)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        """
        Convert the FlaskChestSQLite instance to a dictionary.

        Returns:
            dict: A dictionary representation of the FlaskChestSQLite instance.

        """
        return {"db_uri": self.db_uri}

    def register_table(self, table_name: str = None) -> None:
        """
        Register the SQLite table.

        Args:
            table_name (str, optional): The name of the SQLite table. If not provided, the default table name "flask_chest" will be used.

        Raises:
            Exception: If an error occurs when registering the table.

        """
        try:
            if table_name is not None:
                DEFAULT_SCHEMA["name"] = table_name

            table_exists = create_sqlite_table(self.db_uri, DEFAULT_SCHEMA)

            if not table_exists:
                raise Exception("Unable to register table!")

        except Exception:
            print(traceback.print_exc())
            raise Exception("Error occurred when registering table!")

    def write(
        self,
        variable_name: str,
        variable_value: str,
        request_id: str = None,
    ) -> None:
        """
        Write a key-value pair to the SQLite database.

        Args:
            variable_name (str): The name of the variable.
            variable_value (str): The value of the variable.
            request_id (str, optional): The ID of the request. Defaults to None.

        Raises:
            Exception: If an error occurs when writing to the database.

        """
        try:
            successful_write: bool = sqlite_write(
                self.db_uri,
                DEFAULT_SCHEMA,
                variable_name,
                variable_value,
                request_id,
            )

            if not successful_write:
                raise Exception("Unable to write to database!")

        except Exception:
            print(traceback.print_exc())
            raise Exception("Error occurred when writing to database!")
