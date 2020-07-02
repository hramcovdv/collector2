""" NMAP scan module
"""
from __future__ import absolute_import, unicode_literals
from nmap import PortScanner
from collector.celery import app


@app.task
def ping_scan(hosts):
    """ Ping-scan task
    """
    net_map = PortScanner()
    net_map.scan(hosts, arguments='-sn')

    return net_map.all_hosts()
