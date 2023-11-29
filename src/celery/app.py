'''celery init module'''
from celery import Celery
from src.core.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


celery_app = Celery(
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    include=["src.celery.worker"],
    broker_transport_options={
        'max_retries': 1,
        'visibility_timeout': 365*24*60*60,
    }
)
