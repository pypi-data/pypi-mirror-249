import json
import logging
import time
import traceback

from flask import Flask
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from .base import FlaskChest


class FlaskChestInfluxDB(FlaskChest):
    def __init__(
        self,
        app: Flask,
        https=False,
        host="localhost",
        port=8086,
        token="",
        org="my-org",
        bucket="my-bucket",
        custom_tags={},
        logger=None,
    ):
        super().__init__(app)
        http_scheme = "https" if https else "http"
        self.db_uri = f"{http_scheme}://{host}:{port}"
        self.token = token
        self.org = org
        self.bucket = bucket
        self.custom_tags = custom_tags
        self.logger = logger or logging.getLogger(__name__)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        return {
            "type": "influxdb",
            "db_uri": self.db_uri,
            "bucket": self.bucket,
            "org": self.org,
            "custom_tags": self.custom_tags,
            "log_level": self.log_level,
        }

    def write(
        self,
        context_tuple_list: list,
    ) -> None:
        try:
            if self.logger.level == logging.DEBUG:
                self.logger.debug("FlaskChestInfluxDB: Writing to InfluxDB...")
                self.logger.debug(
                    f"FlaskChestInfluxDB: Context tuple list: {context_tuple_list}"
                )

            data_point_list = []
            for context_tuple in context_tuple_list:
                variable_name, variable_value, request_id = context_tuple

                # Create a data point compatible with InfluxDB
                data_point = create_influxdb_datapoint(
                    variable_name, variable_value, request_id, self.custom_tags
                )

                data_point_list.append(data_point)

            # Create a client to connect to InfluxDB
            client = InfluxDBClient(
                url=self.db_uri, token=self.token, org=self.org, debug=False
            )

            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=self.bucket, org=self.org, record=data_point_list)

        except Exception:
            if self.logger.level == logging.DEBUG:
                self.logger.debug(f"FlaskChestInfluxDB: {traceback.format_exc()}")
            self.logger.error(
                "FlaskChestInfluxDB: Error occurred when writing to InfluxDB!"
            )
            raise Exception("Error occurred when writing to InfluxDB!")


def create_influxdb_datapoint(
    variable_name: str,
    variable_value: str,
    request_id: str = None,
    custom_tags: dict = {},
):
    data_point = {
        "measurement": variable_name,
        "tags": {"request_id": request_id, **custom_tags},
        "fields": {
            "value": variable_value,
        },
        "time": int(time.time() * 1e9),
    }

    return data_point
