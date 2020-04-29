import os
from celery import Celery

os.environ['DJANGO_SETTINGS_MODULE'] = 'bad_shop.settings'

app = Celery('bad_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()