""" SNMP components module
"""
import logging
from pysnmp.smi import builder, view, compiler
from pysnmp.hlapi import getCmd, nextCmd, ObjectIdentity, ObjectType
from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData


MIB_BUILDER = builder.MibBuilder()
compiler.addMibCompiler(MIB_BUILDER, sources=['file:///usr/share/snmp/mibs'])
MIB_BUILDER.loadModules()

MIB_VIEW = view.MibViewController(MIB_BUILDER)


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


def snmp_walk(oids, hostname, community='public', lockup_mib=False):
    """ PySNMP WALK implementation
    """
    response = []

    for (error_indication,
         error_status,
         error_index,
         var_binds) in nextCmd(SnmpEngine(),
                               CommunityData(community, mpModel=1),
                               UdpTransportTarget((hostname, 161), timeout=3, retries=0),
                               ContextData(),
                               *get_var_binds(oids),
                               lexicographicMode=False,
                               lookupMib=lockup_mib):
        if error_indication:
            logging.info('%s - %s', hostname, error_indication)
            break

        if error_status:
            logging.info('%s - %s at %s',
                          hostname,
                          error_status.prettyPrint(),
                          error_index and var_binds[int(error_index) - 1][0] or '?')
            break

        for var_name, var_value in var_binds:
            (_,
             object_name,
             object_instance_id) = MIB_VIEW.getNodeLocation(var_name)

            response.append((object_name,
                             object_instance_id.prettyPrint(),
                             var_value.prettyPrint()))

    return response


def snmp_get(oids, hostname, community='public', lockup_mib=False):
    """ PySNMP GET implementation
    """
    response = []

    session = getCmd(SnmpEngine(),
                     CommunityData(community, mpModel=1),
                     UdpTransportTarget((hostname, 161)),
                     ContextData(),
                     lookupMib=lockup_mib)

    next(session)

    queue = [(oid,) for oid in get_var_binds(oids)]

    while queue:
        error_indication, error_status, error_index, var_binds = session.send(queue.pop())

        if error_indication:
            logging.info('%s - %s', hostname, error_indication)
            break

        if error_status:
            logging.info('%s - %s at %s',
                          hostname,
                          error_status.prettyPrint(),
                          error_index and var_binds[int(error_index)-1][0] or '?')
            break

        for var_name, var_value in var_binds:
            (_,
             object_name,
             object_instance_id) = MIB_VIEW.getNodeLocation(var_name)

            response.append((object_name,
                             object_instance_id.prettyPrint(),
                             var_value.prettyPrint()))

    return response
