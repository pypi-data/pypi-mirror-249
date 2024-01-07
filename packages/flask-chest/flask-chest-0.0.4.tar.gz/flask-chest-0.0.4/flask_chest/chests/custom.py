import json
import logging
import time
import traceback

import requests
from flask import Flask

from .base import FlaskChest


class FlaskChestCustomWriter(FlaskChest):
    """Payload generator is must be a function that takes variable_name, variable_value, and request_id as arguments and returns a dictionary
    which will be used as the payload for the POST request to the custom writer"""

    def __init__(
        self,
        app: Flask,
        https=False,
        host="localhost",
        port="",
        headers=None,
        payload_generator=None,
        verify=False,
        success_status_codes=[200],
        logger=None,
    ):
        super().__init__(app)
        http_scheme = "https" if https else "http"
        self.url = f"{http_scheme}://{host}:{port}"
        self.headers = headers
        self.payload_generator = payload_generator
        self.verify = verify
        self.success_status_codes = success_status_codes
        self.logger = logger

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        return {
            "type": "custom_writer",
            "url": self.url,
            "headers": self.headers,
            "verify": self.verify,
            "success_status_codes": self.success_status_codes,
        }

    def write(
        self,
        context_tuple_list: list,
    ) -> None:
        if self.logger.level == logging.DEBUG:
            self.logger.debug("FlaskChestCustomWriter: Writing to custom writer...")
            self.logger.debug(
                f"FlaskChestCustomWriter: Context tuple list: {context_tuple_list}"
            )
        # Build the payload
        payload = self.payload_generator(context_tuple_list)

        # Send the POST request
        response = requests.post(
            self.url,
            headers=self.headers,
            json=payload,
            verify=self.verify,
        )

        if (
            self.logger.level == logging.DEBUG
            and response.status_code in self.success_status_codes
        ):
            self.logger.debug(
                f"FlaskChestCustomWriter: Status code {response.status_code} received from custom writer!"
            )
        else:
            raise Exception(
                f"FlaskChestCustomWriter: Status code {response.status_code} not in success status codes {self.success_status_codes}!"
            )
