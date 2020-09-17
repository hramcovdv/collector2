""" SNMP components module
"""
from __future__ import absolute_import, unicode_literals
import logging
from collections import defaultdict
from pysnmp.hlapi import getCmd, nextCmd, ObjectIdentity, ObjectType
from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData
from collector.celery import app, mib_view


def get_var_binds(oids):
    """ Return list of ObjectType class instances
    """
    var_binds = []

    for oid in oids:
        if isinstance(oid, (tuple, list)):
            ident = ObjectIdentity(*oid)
        if isinstance(oid, str):
            ident = ObjectIdentity(oid)

        var_binds.append(ObjectType(ident))

    return var_binds


@app.task(name='snmp.snmp_get', ignore_result=True)
def snmp_get(oids, hostname, community='public'):
    """ PySNMP GET implementation
    """
    response = defaultdict(dict)

    session = getCmd(SnmpEngine(),
                     CommunityData(community, mpModel=1),
                     UdpTransportTarget((hostname, 161), timeout=3, retries=1),
                     ContextData(),
                     *get_var_binds(oids),
                     lookupMib=False)

    for error_indication, error_status, error_index, var_binds in session:
        if error_indication:
            logging.warning('%s - %s', hostname, error_indication)
            break

        if error_status:
            logging.warning('%s - %s at %s',
                            hostname,
                            error_status.prettyPrint(),
                            error_index and var_binds[int(error_index)-1][0] or '?')
            break

        for var_name, var_value in var_binds:
            (_, object_name, object_id) = mib_view.getNodeLocation(var_name)

            response[object_id.prettyPrint()].update({object_name: var_value.prettyPrint()})

    return dict(response)


@app.task(name='snmp.snmp_walk', ignore_result=True)
def snmp_walk(oids, hostname, community='public'):
    """ PySNMP WALK implementation
    """
    response = defaultdict(dict)

    session = nextCmd(SnmpEngine(),
                      CommunityData(community, mpModel=1),
                      UdpTransportTarget((hostname, 161), timeout=3, retries=1),
                      ContextData(),
                      *get_var_binds(oids),
                      lexicographicMode=False,
                      lookupMib=False)

    for error_indication, error_status, error_index, var_binds in session:
        if error_indication:
            logging.warning('%s - %s', hostname, error_indication)
            break

        if error_status:
            logging.warning('%s - %s at %s',
                            hostname,
                            error_status.prettyPrint(),
                            error_index and var_binds[int(error_index)-1][0] or '?')
            break

        for var_name, var_value in var_binds:
            (_, object_name, object_id) = mib_view.getNodeLocation(var_name)

            response[object_id.prettyPrint()].update({object_name: var_value.prettyPrint()})

    return dict(response)
