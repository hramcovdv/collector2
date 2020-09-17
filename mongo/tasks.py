""" MongoDB tasks module
"""
from __future__ import absolute_import, unicode_literals
from datetime import datetime
from collector.celery import app
from collector.celery import mongo_database as db


@app.task
def get_hosts(find=None):
    """ Get hosts from DB
    """
    find = find or {}
    hosts = db['hosts']

    return hosts.find(find, {'_id': False}, sort=[('address', 1),])


@app.task(ignore_result=True)
def write_host(address, data=None):
    """ Write hosts to DB
    """
    data = data or {}
    hosts = db['hosts']

    data.update({'lastcheck': datetime.now()})

    result = hosts.find_one_and_update({'address': address}, {'$set': data})

    if result is None:
        hosts.insert_one({
            'address': address,
            'location': data.get('location', 'Orenburg'),
            'latitude': data.get('latitude', 51.768199),
            'longitude': data.get('longitude', 55.096955),
            'community': data.get('community', 'public'),
            'observe': data.get('observe', True),
            'lastcheck': data.get('lastcheck')
        })
