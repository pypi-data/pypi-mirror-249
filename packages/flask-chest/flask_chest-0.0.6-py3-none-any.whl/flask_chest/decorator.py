# decorator.py

import uuid
from functools import wraps
from typing import Callable, List, Optional

from flask import current_app, g, request
from icecream import ic

from flask_chest import FlaskChest


def flask_chest(
    chests: List[FlaskChest],
    tracked_vars: List[str],
    request_id_generator=None,
    raise_exceptions: bool = True,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            set_custom_request_id(request_id_generator)
            response = func(*args, **kwargs)
            write_tracked_variables(chests, tracked_vars, raise_exceptions)
            return response

        return wrapper

    return decorator


def write_tracked_variables(
    chests: List[FlaskChest], tracked_vars: List[str], raise_exceptions: bool
) -> None:
    # Write tracked variables to each chest
    for chest in chests:
        request_id = getattr(g, "custom_request_id", None)
        # Write tracked variables to database
        for request_method, context_vars in tracked_vars.items():
            if request.method == request_method.upper():
                # For each global context var in the list of tracked vars
                context_tuple_list = []
                for var_name in context_vars:
                    if hasattr(g, var_name):
                        value = getattr(g, var_name)
                        context_tuple_list.append((var_name, value, request_id))
                if raise_exceptions:
                    try:
                        # Generic write for all chest types
                        chest.write(context_tuple_list)
                    except Exception as e:
                        raise e
                else:
                    try:
                        # Generic write for all chest types
                        chest.write(context_tuple_list)
                    except Exception as e:
                        if chest.logger:
                            chest.logger.debug(e)


def set_custom_request_id(request_id_generator):
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
