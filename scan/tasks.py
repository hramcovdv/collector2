""" ICMP tasks module
"""
from __future__ import absolute_import, unicode_literals
import ipcalc
from icmplib import ping
from collector.celery import app

from .helper import is_alive


@app.task
def ping_host(address, count=5, interval=1, timeout=1):
    """ Ping host task
    """
    host = ping(
        address=address,
        count=count,
        interval=interval,
        timeout=timeout
    )

    return {
        'min_rtt': host.min_rtt,
        'avg_rtt': host.avg_rtt,
        'max_rtt': host.max_rtt,
        'packets_sent': host.packets_sent,
        'packets_received': host.packets_received,
        'packet_loss': host.packet_loss
    }


@app.task
def find_hosts(network):
    """ Find hosts in network
    """
    return [str(host) for host in ipcalc.Network(network) if is_alive(host)]
