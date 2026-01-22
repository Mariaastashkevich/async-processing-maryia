from celery import Celery
from services.settings import settings


celery_app = Celery(
    'async_processing',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.autodiscover_tasks(["workers"])

import workers.jobs