""" Celery tasks module
"""
from __future__ import absolute_import, unicode_literals
from celery import group, chain
from collector.celery import app
from collector.scan.tasks import ping_host, find_hosts
from collector.snmp.tasks import snmp_get, snmp_walk
from collector.mongo.tasks import get_hosts, write_host
from collector.influx.tasks import write_uptime, write_iftable, write_icmp


@app.task(name='schedule.collect_uptime')
def collect_uptime():
    """ Collect system task
    """
    oids = [
        ('SNMPv2-MIB', 'sysUpTime', 0)
    ]

    group(
        chain(
            snmp_get.s(
                oids=oids,
                hostname=host['address'],
                community=host['community']
            ),
            write_uptime.s(tags={'host': host['address']})
        ) for host in get_hosts({'observe': True})
    )()


@app.task(name='schedule.collect_iftable')
def collect_iftable():
    """ Collect ifTable task
    """
    oids = [
        ('IF-MIB', 'ifName'),
        ('IF-MIB', 'ifType'),
        ('IF-MIB', 'ifAdminStatus'),
        ('IF-MIB', 'ifOperStatus'),
        ('IF-MIB', 'ifInOctets'),
        ('IF-MIB', 'ifInMulticastPkts'),
        ('IF-MIB', 'ifInBroadcastPkts'),
        ('IF-MIB', 'ifInUcastPkts'),
        ('IF-MIB', 'ifInNUcastPkts'),
        ('IF-MIB', 'ifInDiscards'),
        ('IF-MIB', 'ifInErrors'),
        ('IF-MIB', 'ifOutOctets'),
        ('IF-MIB', 'ifOutMulticastPkts'),
        ('IF-MIB', 'ifOutBroadcastPkts'),
        ('IF-MIB', 'ifOutUcastPkts'),
        ('IF-MIB', 'ifOutNUcastPkts'),
        ('IF-MIB', 'ifOutDiscards'),
        ('IF-MIB', 'ifOutErrors')
    ]

    group(
        chain(
            snmp_walk.s(
                oids=oids,
                hostname=host['address'],
                community=host['community']
            ),
            write_iftable.s(
                tags={
                    'host': host['address'],
                    'location': host['location']
                }
            )
        ) for host in get_hosts({'observe': True})
    )()


@app.task(name='schedule.collect_icmp')
def collect_icmp():
    """ Collect ICMP task
    """
    group(
        chain(
            ping_host.s(
                address=host['address']
            ),
            write_icmp.s(
                tags={
                    'host': host['address'],
                    'location': host['location'],
                    'latitude': host['latitude'],
                    'longitude': host['longitude']
                }
            )
        ) for host in get_hosts({'observe': True})
    )()


@app.task(name='schedule.collect_hosts')
def collect_hosts(network):
    """ Find hosts and get location
    """
    for host in find_hosts(network):
        write_host(host)
