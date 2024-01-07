from flask import Flask

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
            app.extensions["flask_chest"] = [self]
        else:
            if "flask_chest" not in app.extensions:
                app.extensions["flask_chest"] = [self]
            else:
                app.extensions["flask_chest"].append(self)