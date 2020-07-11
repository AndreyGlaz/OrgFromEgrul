from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OrgFromEgrul.settings')
app = Celery('OrgFromEgrul')

app.conf.update(
    broker_url='redis://192.168.99.100:6379/0',
    result_backend='redis://192.168.99.100:6379/0',
    task_track_started=True,
    timezone='Europe/Moscow',
    worker_disable_rate_limits=True,
    beat_schedule={
        'update_data': {
            'task': 'OrgFromEgrul.tasks.start_update',
            # 'schedule': 100.0,
            'schedule': crontab(minute=24, hour=11),
        }
    }
)

app.autodiscover_tasks(['OrgFromEgrul'])
