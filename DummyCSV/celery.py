import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DummyCSV.settings')
app = Celery('DummyCSV')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(BROKER_URL=os.getenv('REDIS_URL'),
                CELERY_RESULT_BACKEND=os.getenv('REDIS_URL'))

app.autodiscover_tasks()