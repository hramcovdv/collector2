""" Celery config module
"""
from kombu import Queue
# from celery.schedules import crontab


BROKER_URL = 'redis://{hostname}:{port}/{db}'.format(
    hostname='localhost',
    port=6379,
    db=9
)

CELERY_RESULT_BACKEND = BROKER_URL
CELERY_RESULT_EXPIRES = 3600

# CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 2

CELERY_IMPORTS = (
    'collector.cron.tasks',
    'collector.scan.tasks',
    'collector.snmp.tasks',
    'collector.influx.tasks'
)

CELERY_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('service', routing_key='service')
)

CELERY_DEFAULT_QUEUE = 'default'

CELERY_ROUTES = {
    'collector.cron.tasks.*': {
        'queue': 'service'
    },
    'collector.influx.tasks.*': {
        'queue': 'service'
    }
}

CELERYBEAT_SCHEDULE = {
    'collect-iftable-every-1min': {
        'task': 'collector.cron.tasks.collect_iftable',
        'schedule': 60.0,
        'args': ('10.10.8.0/25', 60)
    },
    'collect-system-every-1min': {
        'task': 'collector.cron.tasks.collect_system',
        'schedule': 60.0,
        'args': ('10.10.8.0/25', 60)
    },
    'collect-icmp-every-30sec': {
        'task': 'collector.cron.tasks.collect_icmp',
        'schedule': 30.0,
        'args': ('10.10.8.0/25', 30)
    }
}
