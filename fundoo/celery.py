from __future__ import absolute_import, unicode_literals
import os
import sys
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

sys.path.append(os.path.abspath('fundoo'))
# app = Celery('Fundoo')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fundoo.settings')
app = Celery('hello', broker="amqp://guest@localhost//")
app.conf.beat_schedule = {
    'test-task': {
        'task': 'tasks.email',
        'schedule': crontab(),
    },
}
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()