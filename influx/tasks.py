""" InfluxDB store module
"""
from __future__ import absolute_import, unicode_literals
from collector.celery import app
from collector.celery import influx_client as client

from .helper import SeriesHelper


@app.task(name='influx.write_uptime', ignore_result=True)
def write_uptime(items, tags=None):
    """ Write uptime
    """
    series = SeriesHelper(client, measurement='system')

    series.add_points(items.values())
    series.write_points(tags=tags, time_precision='s')


@app.task(name='influx.write_iftable', ignore_result=True)
def write_iftable(items, tags=None):
    """ Write ifTable
    """
    series = SeriesHelper(
        client,
        measurement='ifTable',
        tags=['ifName', 'ifType']
    )

    series.add_points(items.values())
    series.write_points(tags=tags, time_precision='s')


@app.task(name='influx.write_icmp', ignore_result=True)
def write_icmp(item, tags=None):
    """ Write ICMP result
    """
    if item is None:
        return

    series = SeriesHelper(client, measurement='icmp')

    series.add_point(item)
    series.write_points(tags=tags, time_precision='s')
