import json
import traceback
import time
from icecream import ic

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
        debug=False,
    ):
        super().__init__(app)
        http_scheme = "https" if https else "http"
        self.db_uri = f"{http_scheme}://{host}:{port}"
        self.token = token
        self.org = org
        self.bucket = bucket
        self.debug = debug

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        return {"type": "influxdb",
                "db_uri": self.db_uri}
        
    def write(
        self,
        context_tuple_list: list,
    ) -> None:
        try:
            
            data_point_list = []
            for context_tuple in context_tuple_list:
                variable_name, variable_value, request_id = context_tuple
            
                # Create a data point compatible with InfluxDB
                data_point = create_influxdb_datapoint(
                    variable_name,
                    variable_value,
                    request_id
                )
                
                data_point_list.append(data_point)
            
            # Create a client to connect to InfluxDB
            client = InfluxDBClient(
                url=self.db_uri,
                token=self.token,
                org=self.org,
                debug=self.debug,
            )
            
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=self.bucket, org=self.org, record=data_point_list)

        except Exception:
            print(traceback.print_exc())
            raise Exception("Error occurred when writing to InfluxDB!")
        
    
def create_influxdb_datapoint(
    variable_name: str,
    variable_value: str,
    request_id: str = None,
):
    data_point = {
        "measurement": variable_name,
        "tags": {
            "request_id": request_id,
        },
        "fields": {
            "value": variable_value,
        },
        "time": int(time.time() * 1e9),
    }
    
    return data_point