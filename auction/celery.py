from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction.settings')
app = Celery('auction')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

from celery.schedules import crontab
app.conf.beat_schedule = {

    # 'add-every-5-seconds': {
    #     'task': 'multiply_two_numbers',
    #     'schedule': 5.0,
    #     'args': (16, 16)
    # },
    # 'add-every-30-seconds': {
    #     'task': 'multiply_two_numbers',
    #     'schedule': 10.0,
    #     'args': (3, 1)
    # },
    'every-60-secs':{
        'task':'call the models',
        'schedule':20.0,

    }
}
