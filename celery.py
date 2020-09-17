""" Celery app module
"""
from __future__ import absolute_import, unicode_literals
import os
from dotenv import load_dotenv
from influxdb import InfluxDBClient
from pymongo import MongoClient
from pysnmp.smi import builder, view, compiler
from celery import Celery


load_dotenv()

BROKER_URL = 'redis://{hostname}:{port}/{db}'.format(
    hostname=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    db=os.getenv('REDIS_DB')
)

BACKEND_URL = BROKER_URL

mib_builder = builder.MibBuilder()
compiler.addMibCompiler(mib_builder, sources=['file:///usr/share/snmp/mibs'])
mib_builder.loadModules()

mib_view = view.MibViewController(mib_builder)

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
