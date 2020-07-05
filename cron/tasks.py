""" Scheduled tasks module
"""
from __future__ import absolute_import, unicode_literals
import ipcalc
from celery import group, chain
from collector.celery import app
from collector.scan.tasks import ping_host
from collector.snmp.tasks import walk_iftable, get_system
from collector.influx.tasks import write_iftable, write_system, write_icmp


@app.task(ignore_result=True)
def collect_iftable(network, ex=None):
    """ Collect ifTable task
    """
    hosts = [str(ip) for ip in ipcalc.Network(network)]

    group(
        chain(
            walk_iftable.s(
                hostname=host
            ).set(expires=ex),
            write_iftable.s(
                tags={'Agent': host}
            ).set(expires=ex)
        ) for host in hosts
    )()


@app.task(ignore_result=True)
def collect_system(network, ex=None):
    """ Collect system task
    """
    hosts = [str(ip) for ip in ipcalc.Network(network)]

    group(
        chain(
            get_system.s(
                hostname=host
            ).set(expires=ex),
            write_system.s(
                tags={'Agent': host}
            ).set(expires=ex)
        ) for host in hosts
    )()


@app.task(ignore_result=True)
def collect_icmp(network, ex=None):
    """ Collect ICMP task
    """
    hosts = [str(ip) for ip in ipcalc.Network(network)]

    group(
        chain(
            ping_host.s(
                address=host,
                count=10,
                interval=0.5,
                timeout=2
            ).set(expires=ex),
            write_icmp.s(
                tags={'host': host}
            ).set(expires=ex)
        ) for host in hosts
    )()
