""" Celery app module
"""
from __future__ import absolute_import, unicode_literals
import os
from dotenv import load_dotenv
from influxdb import InfluxDBClient
from pymongo import MongoClient
from celery import Celery
# from celery.schedules import crontab

load_dotenv()

BROKER_URL = 'redis://{hostname}:{port}/{db}'.format(
    hostname=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    db=os.getenv('REDIS_DB')
)

BACKEND_URL = BROKER_URL

influx_client = InfluxDBClient(
    host=os.getenv('INFLUXDB_HOST'),
    port=os.getenv('INFLUXDB_PORT'),
    username=os.getenv('INFLUXDB_USER'),
    password=os.getenv('INFLUXDB_PSWD'),
    database=os.getenv('APP_NAME')
)

mongo_client = MongoClient('mongodb://{username}:{password}@{host}:{port}'.format(
    host=os.getenv('MONGODB_HOST'),
    port=os.getenv('MONGODB_PORT'),
    username=os.getenv('MONGODB_USER'),
    password=os.getenv('MONGODB_PSWD'),
))

mongo_database = mongo_client[os.getenv('APP_NAME')]

app = Celery(
    os.getenv('APP_NAME'),
    broker=BROKER_URL,
    backend=BACKEND_URL
)

app.config_from_object('collector.celeryconfig')

app.conf.beat_schedule = {
    'collect-iftable-every-1min': {
        'task': 'collector.cron.tasks.collect_iftable',
        'schedule': 60.0,
        'kwargs': (ex=60,)
    },
    'collect-system-every-1min': {
        'task': 'collector.cron.tasks.collect_system',
        'schedule': 60.0,
        'kwargs': (ex=60,)
    },
    'collect-icmp-every-1min': {
        'task': 'collector.cron.tasks.collect_icmp',
        'schedule': 30.0,
        'kwargs': (ex=60,)
    }
}
