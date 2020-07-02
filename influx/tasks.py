""" InfluxDB store module
"""
from __future__ import absolute_import, unicode_literals
from collector.celery import app
from collector.celery import influx_client as client

from .helper import SeriesHelper


@app.task(ignore_result=True)
def write_iftable(items, tags=None):
    """ Write ifTable task
    """
    series = SeriesHelper(client,
                          'ifTable',
                          tags=['ifName', 'ifType'],
                          fields=['ifAdminStatus',
                                  'ifOperStatus',
                                  'ifInOctets',
                                  'ifInMulticastPkts',
                                  'ifInBroadcastPkts',
                                  'ifInUcastPkts',
                                  'ifInNUcastPkts',
                                  'ifInDiscards',
                                  'ifInErrors',
                                  'ifOutOctets',
                                  'ifOutMulticastPkts',
                                  'ifOutBroadcastPkts',
                                  'ifOutUcastPkts',
                                  'ifOutNUcastPkts',
                                  'ifOutDiscards',
                                  'ifOutErrors'])

    series.add_points(items)
    series.write_points(tags=tags, time_precision='s')
