from __future__ import absolute_import, unicode_literals

import os

# import django
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrgFromEgrul.settings')
# django.setup()
app = Celery('OrgFromEgrul')

app.conf.update(
    broker_url='redis://192.168.99.100:6379/0',
    timezone='Europe/Moscow',
    beat_schedule={
        'add-every-30-seconds': {
            'task': 'OrgFromEgrul.tasks.debug_task',
            # 'schedule': 100.0,
            'schedule': crontab(minute=6, hour=16),
        }
    }
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['OrgFromEgrul'])
