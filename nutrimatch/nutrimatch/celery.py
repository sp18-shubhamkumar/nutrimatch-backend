import os
from celery import Celery
from decouple import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutrimatch.settings')

app = Celery('nutrimatch')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = config('CELERY_BROKER_URL')
app.conf.result_backend = config('CELERY_RESULT_BACKEND')
app.autodiscover_tasks()

