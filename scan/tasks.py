""" ICMP tasks module
"""
from __future__ import absolute_import, unicode_literals
from icmplib import ping
from collector.celery import app


@app.task
def ping_host(address, **kwargs):
    """ Ping host task
    """
    host = ping(address, **kwargs)

    if host.is_alive:
        return {
            'min_rtt': host.min_rtt,
            'avg_rtt': host.avg_rtt,
            'max_rtt': host.max_rtt,
            'packets_sent': host.packets_sent,
            'packets_received': host.packets_received,
            'packet_loss': host.packet_loss
        }

    return {}
