""" SNMP tasks module
"""
from __future__ import absolute_import, unicode_literals
from collections import defaultdict
from collector.celery import app

from .helper import snmp_walk, snmp_get


IF_TABLE_OIDS = [
    # ('IF-MIB', 'ifIndex'),
    ('IF-MIB', 'ifName'),
    ('IF-MIB', 'ifType'),
    # ('IF-MIB', 'ifMtu'),
    # ('IF-MIB', 'ifSpeed'),
    # ('IF-MIB', 'ifLastChange'),
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
    ('IF-MIB', 'ifOutErrors'),
]

SYSTEM_OIDS = [('SNMPv2-MIB', 'sysUpTime', 0)]


def grouping(items):
    """ Grouping oid, index and value by index
    """
    grouped = defaultdict(dict)

    for oid, index, value in items:
        grouped[index][oid] = value

    return list(grouped.values())


@app.task
def walk_iftable(hostname, *options):
    """ Walk ifTable task
    """
    return grouping(snmp_walk(IF_TABLE_OIDS, hostname, *options))


@app.task
def get_system(hostname, *options):
    """ Get system task
    """
    return grouping(snmp_get(SYSTEM_OIDS, hostname, *options))
