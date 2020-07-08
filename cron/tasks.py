""" Scheduled tasks module
"""
from __future__ import absolute_import, unicode_literals
from celery import group, chain
from collector.celery import app
from collector.scan.tasks import ping_host
from collector.snmp.tasks import walk_iftable, get_system
from collector.mongo.tasks import get_hosts
from collector.influx.tasks import write_iftable, write_system, write_icmp


@app.task(ignore_result=True)
def collect_iftable(ex=None):
    """ Collect ifTable task
    """
    group(
        chain(
            walk_iftable.s(
                host['address'],
                community=host['community']
            ).set(expires=ex),
            write_iftable.s(
                tags={'host': host['address']}
            ).set(expires=ex)
        ) for host in get_hosts()
    )()


@app.task(ignore_result=True)
def collect_system(ex=None):
    """ Collect system task
    """
    group(
        chain(
            get_system.s(
                host['address'],
                community=host['community']
            ).set(expires=ex),
            write_system.s(
                tags={'host': host['address']}
            ).set(expires=ex)
        ) for host in get_hosts()
    )()


@app.task(ignore_result=True)
def collect_icmp(ex=None):
    """ Collect ICMP task
    """
    group(
        chain(
            ping_host.s(
                host['address'],
                count=5,
                interval=1,
                timeout=2
            ).set(expires=ex),
            write_icmp.s(
                tags={'host': host['address']}
            ).set(expires=ex)
        ) for host in get_hosts()
    )()
