""" Celery config module
"""
# from kombu import Queue

CELERY_IMPORTS = (
    'collector.cron.tasks',
    'collector.scan.tasks',
    'collector.snmp.tasks',
    'collector.mongo.tasks',
    'collector.influx.tasks'
)

# CELERY_QUEUES = (
#     Queue('default', routing_key='default'),
#     Queue('influx', routing_key='influx'),
#     Queue('cron', routing_key='cron'),
#     Queue('snmp', routing_key='snmp'),
# )

CELERY_DEFAULT_QUEUE = 'default'

CELERY_ROUTES = {
    'collector.influx.tasks.*': {
        'queue': 'influx'
    },
    'collector.cron.tasks.*': {
        'queue': 'cron'
    },
    'collector.snmp.tasks.*': {
        'queue': 'snmp'
    }
}

CELERY_RESULT_EXPIRES = 3600

CELERY_ACKS_LATE = True

CELERYD_PREFETCH_MULTIPLIER = 1
