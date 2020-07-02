""" Scheduled tasks module
"""
from __future__ import absolute_import, unicode_literals
from celery import group, chain
from collector.celery import app
from collector.scan.tasks import ping_scan
from collector.snmp.tasks import walk_iftable
from collector.influx.tasks import write_iftable


@app.task(ignore_result=True)
def collect_iftable(hosts, ex=None):
    """ Collect ifTable task
    """
    group(
        chain(
            walk_iftable.s(
                hostname=host
            ).set(expires=ex),
            write_iftable.s(
                tags={'Agent': host}
            ).set(expires=ex)
        ) for host in ping_scan(hosts)
    )()
