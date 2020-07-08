""" MongoDB tasks module
"""
from __future__ import absolute_import, unicode_literals
from collector.celery import app
from collector.celery import mongo_database as db


@app.task
def get_hosts(find=None):
    """ Get hosts task
    """
    find = find if find else {}
    collection = db['hosts']

    return collection.find(find,
                           {'_id': False},
                           sort=[('address', 1)])
