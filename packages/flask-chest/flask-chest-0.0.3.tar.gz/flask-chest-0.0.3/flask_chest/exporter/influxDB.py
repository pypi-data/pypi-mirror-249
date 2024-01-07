import logging
import sqlite3
import threading
import time

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from .base import FlaskChestExporter

# Create a lock object
lock = threading.Lock()


class FlaskChestExporterInfluxDB(FlaskChestExporter):
    def __init__(
        self,
        chest,
        https=False,
        host="localhost",
        port=8086,
        token="",
        org="my-org",
        bucket="my-bucket",
        interval_minutes=5,
    ):
        """
        Initializes a FlaskChestExporterInfluxDB instance.

        Parameters:
        - chest: The FlaskChest instance.
        - https: Whether to use HTTPS for the InfluxDB connection (default: False).
        - host: The InfluxDB host (default: "localhost").
        - port: The InfluxDB port (default: 8086).
        - token: The InfluxDB authentication token (default: "").
        - org: The InfluxDB organization (default: "my-org").
        - bucket: The InfluxDB bucket (default: "my-bucket").
        - interval_minutes: The interval in minutes for exporting data (default: 5).

        Returns:
        None
        """
        super().__init__(chest, interval_minutes=interval_minutes)
        http_scheme = "https" if https else "http"
        self.client = InfluxDBClient(
            url=f"{http_scheme}://{host}:{port}",
            token=token,
            org=org,
            debug=False,
        )
        self.chest = chest
        self.org = org
        self.bucket = bucket
        self.start_export_task()

    def export_data(self):
        """
        The function "export_data" is used to export data from flask_chest table to InfluxDB.

        Returns:
        None
        """
        data = self.fetch_data_from_flask_chest()
        self.write_to_influxdb(data)

    def write_to_influxdb(self, data):
        """
        Write data to InfluxDB.

        Parameters:
        - data: The data to be written to InfluxDB.

        Returns:
        None
        """
        try:
            write_api = self.client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=self.bucket, org=self.org, record=data)
            logging.info("Data successfully written to InfluxDB")

        except Exception as e:
            logging.error(f"Error writing data to InfluxDB: {e}")

    def fetch_data_from_flask_chest(self):
        """
        Fetches data from the flask_chest table in the SQLite database and prepares it for InfluxDB.

        Returns:
            list: A list of data points formatted for InfluxDB.

        Raises:
            sqlite3.Error: If there is an error with the SQLite database.
            Exception: If there is an exception during the query execution.
        """
        conn = sqlite3.connect(self.chest.db_uri)
        cursor = conn.cursor()
        query = "SELECT unique_id, request_id, name, value FROM flask_chest"

        try:
            # Acquire the lock before executing the query
            lock.acquire()

            cursor.execute(query)
            rows = cursor.fetchall()
            influxdb_data = []

            # For each row in flask_chest table, create a data point
            for row in rows:
                data_point = {
                    "measurement": "sample",
                    "tags": {
                        "unique_id": row[0],
                        "request_id": row[1],
                    },
                    "fields": {
                        "name": row[2],
                        "value": row[3],
                    },
                    "time": int(time.time() * 1e9),
                }
                influxdb_data.append(data_point)

            # Remove rows from flask_chest table
            cursor.execute("DELETE FROM flask_chest")
            conn.commit()

            return influxdb_data
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in query: {e}")
        finally:
            # Release the lock after executing the query
            lock.release()
            cursor.close()
            conn.close()
