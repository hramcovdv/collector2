""" Celery app module
"""
from __future__ import absolute_import, unicode_literals
import os
from dotenv import load_dotenv
from influxdb import InfluxDBClient
from celery import Celery


load_dotenv()

app = Celery('collector')
app.config_from_object('collector.celeryconfig')

influx_client = InfluxDBClient(
    host=os.getenv('INFLUXDB_HOST'),
    port=os.getenv('INFLUXDB_PORT'),
    username=os.getenv('INFLUXDB_USER'),
    password=os.getenv('INFLUXDB_PSWD'),
    database=os.getenv('INFLUXDB_DB')
)


if __name__ == '__main__':
    app.start()
