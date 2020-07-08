""" SNMP tasks module
"""
from __future__ import absolute_import, unicode_literals
from collector.celery import app

from .helper import snmp_walk, snmp_get


IFTABLE_OIDS = [
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

SYSTEM_OIDS = [
    ('SNMPv2-MIB', 'sysUpTime', 0)
]


@app.task
def walk_iftable(hostname, **kwargs):
    """ Walk ifTable task
    """
    return snmp_walk(IFTABLE_OIDS, hostname, **kwargs)


@app.task
def get_system(hostname, **kwargs):
    """ Get system task
    """
    return snmp_get(SYSTEM_OIDS, hostname, **kwargs)
