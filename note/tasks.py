
from __future__ import absolute_import, unicode_literals

import datetime
import sys
import redis
import requests
import os
from celery import Celery
from celery.schedules import crontab

app = Celery('hello', broker="amqp://guest@localhost//")
app.conf.beat_schedule = {
    'test-task': {
        'task': 'tasks.email',
        # 'schedule': datetime.timedelta(seconds=55),
    },
}




@app.task()
def email():
    requests.get(url="http://localhost:8000/api/celery",)



