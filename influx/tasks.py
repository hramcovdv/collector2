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
    if items:
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


@app.task(ignore_result=True)
def write_system(items, tags=None):
    """ Write system task
    """
    if items:
        series = SeriesHelper(client,
                              'system',
                              fields=['sysUpTime'])

        series.add_points(items)
        series.write_points(tags=tags, time_precision='s')


@app.task(ignore_result=True)
def write_icmp(item, tags=None):
    """ Write ICMP task
    """
    if item:
        series = SeriesHelper(client,
                              'icmp',
                              fields=['min_rtt',
                                      'avg_rtt',
                                      'max_rtt',
                                      'packets_sent',
                                      'packets_received',
                                      'packet_loss'])

        series.add_point(item)
        series.write_points(tags=tags, time_precision='s')
