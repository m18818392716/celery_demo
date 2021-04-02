from __future__ import absolute_import,unicode_literals
import os
from celery import Celery,platforms
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_demo.settings')

broker = 'redis://localhost:6379/0'
app = Celery('celery_demo',broker=broker)

# app.conf.timezone = 'Asia/Shanghai'

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks(['Admin'], force=True)

platforms.C_FORCE_ROOT = True

@app.task(bind=True)
def debug_task(self):
    print('Request:{0!r}'.format(self.request))