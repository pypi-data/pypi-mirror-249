# Flask-Chest

<center>

![Flask-Chest Icon](/images/flask_chest_README.png)

</center>

<center>

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</center>

## Introduction

Flask-Chest is a Python package for Flask applications, providing a decorator to track and record global context variables (`g.variables`) for each request. It interfaces with various databases to store and export these variables, serving as a tool for monitoring and analytics in Flask web applications.

## Features

- Tracks and records `g.variables` in Flask routes, allowing for the storage of contextual data in a configured database.
- Offers customizable request ID generation, ensuring unique identification of each request for better traceability and analysis of contextual data.
- Provides support for multiple databases, including SQLite, MySQL, PostgreSQL, and MongoDB, enabling flexibility in choosing the appropriate database for the application.
- Implements thread-safe data exporters, scheduled using AP Scheduler, to reliably and periodically export the recorded data, facilitating monitoring and analytics.

## Installation

```bash
pip install flask-chest
```

## Usage

1. Import and initialize a Flask-Chest or multiple Flask-Chest objects in your Flask application.
2. When initializing a Flask-Chest object, provide the desired database and exporter(s) to use for data storage and export.
3. Define which variables should be tracked per route by creating a dictionary where each HTTP method (e.g., "GET", "POST") is a key, and the value is a list of strings representing the names of the variables to track.
4. Provide an iterable containing the Flask-Chest object(s) the decorator should write to each request.
4. Provide a request ID generator function that returns a unique string identifier for each request. If no custom generator is provided, a UUID4 string will be used by default.
5. Apply the `@flask_chest` decorator to Flask routes.

## List of Flask-Chest Objects
- FlaskChestSQLite: Uses a SQLite database to store data.
- FlaskChestInfluxDB: Uses an InfluxDB database to store data.
- FlaskChestCustomWriter: Uses a custom writer to store data, takes params required for a POST request.

## List of Exporters
- FlaskChestExporterInfluxDB: Exports data to an InfluxDB database.

_Coming soon_:
- FlaskChestExporterMongoDB: Exports data to a MongoDB database.
- FlaskChestExporterMySQL: Exports data to a MySQL database.
- FlaskChestExporterPostgreSQL: Exports data to a PostgreSQL database.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
