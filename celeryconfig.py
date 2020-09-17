""" Celery config module
"""
from kombu import Queue
# from celery.schedules import crontab

CELERY_IMPORTS = (
    'collector.celerytasks',
    'collector.scan.tasks',
    'collector.snmp.tasks',
    'collector.mongo.tasks',
    'collector.influx.tasks'
)

CELERY_DEFAULT_QUEUE = 'default'

CELERY_QUEUES = (
    Queue('default'),
    Queue('schedule'),
    Queue('influx'),
    Queue('snmp')
)

CELERY_ROUTES = {
    'schedule.*': {'queue': 'schedule'},
    'influx.*': {'queue': 'influx'},
    'snmp.*': {'queue': 'snmp'}
}

CELERY_TASK_RESULT_EXPIRES = 60 * 60  # 1 hour
# CELERY_ACKS_LATE = True
# CELERYD_PREFETCH_MULTIPLIER = 1

CELERYBEAT_SCHEDULE = {
    'collect-uptime-every-1min': {
        'task': 'schedule.collect_uptime',
        'schedule': 60.0,
    },
    'collect-iftable-every-1min': {
        'task': 'schedule.collect_iftable',
        'schedule': 60.0,
    },
    'collect-icmp-every-30sec': {
        'task': 'schedule.collect_icmp',
        'schedule': 30.0,
    },
    'find-hosts-every-5min': {
        'task': 'schedule.collect_hosts',
        'schedule': 60.0*5,
        'args': ('192.168.0.0/24',)
    }
}
