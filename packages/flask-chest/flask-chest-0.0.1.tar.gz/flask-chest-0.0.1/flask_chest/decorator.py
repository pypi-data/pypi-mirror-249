# decorator.py

import uuid
from functools import wraps
from typing import Callable, List, Optional

from flask import current_app, g, request

from flask_chest import FlaskChestSQLite


def flask_chest(
    tracked_vars: List[str],
    request_id_generator: Optional[Callable[[], str]] = None,
) -> Callable[..., Callable]:
    """
    The `flask_chest` function is a decorator that tracks specified variables and writes them to a table
    in a database after the decorated function is executed.

    :param table_name: The name of the table where the tracked variables will be stored
    :param tracked_vars: The "tracked_vars" parameter is a list of variables that you want to track and store in a
    database table. These variables can be any values that you want to keep track of during the
    execution of the decorated function
    :param request_id_generator: The `request_id_generator` parameter is a function that generates a
    unique request ID for each request. This can be useful for tracking and logging purposes. If no
    `request_id_generator` is provided, the default request ID generator will be used
    :return: The function `decorator` is being returned.
    """

    def decorator(func: Callable[..., Callable]) -> Callable[..., Callable]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            set_custom_request_id(request_id_generator)
            response = func(*args, **kwargs)
            write_tracked_variables(tracked_vars)
            return response

        return wrapper

    return decorator


def set_custom_request_id(request_id_generator: Optional[Callable[[], str]]):
    """
    The function `set_custom_request_id` sets a custom request ID by either using a provided request ID
    generator function or generating a random UUID, and then truncates the ID if it exceeds 255
    characters.

    :param request_id_generator: The `request_id_generator` parameter is a function that generates a
    custom request ID. It should return a unique identifier for each request. If a custom request ID
    generator is not provided, a random UUID (Universally Unique Identifier) will be used instead
    """
    if callable(request_id_generator):
        g.custom_request_id = str(request_id_generator())
    else:
        g.custom_request_id = str(uuid.uuid4())

    # Check if the custom_request_id is too long
    if len(g.custom_request_id) > 255:
        g.custom_request_id = g.custom_request_id[:255]


def write_tracked_variables(tracked_vars: List[str]) -> None:
    """
    The function writes tracked variables to a database using Flask-Chest extension.

    :param tracked_vars: The `tracked_vars` parameter is a string that represents the name of the schema
    or database table where the tracked variables will be written to
    :param tracked: The "tracked" parameter is a dictionary where the keys are HTTP request methods
    (e.g., "GET", "POST", "PUT", etc.) and the values are lists of variable names that you want to track
    for each request method
    """
    # Get Flask-Chest extension
    flask_chest = current_app.extensions.get("flask_chest")
    if flask_chest:
        # Get request ID
        request_id = getattr(g, "custom_request_id", None)
        # Write tracked variables to database
        for request_method, context_vars in tracked_vars.items():
            if request.method == request_method.upper():
                for var in context_vars:
                    if hasattr(g, var):
                        value = getattr(g, var)
                        # If Flask-Chest extension is SQLite, pass table name
                        if isinstance(flask_chest, FlaskChestSQLite):
                            flask_chest.write(var, value, request_id)
    else:
        raise Exception("Flask-Chest extension not found!")
