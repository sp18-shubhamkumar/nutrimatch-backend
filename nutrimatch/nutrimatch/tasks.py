import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def my_background_task():
    logger.info("Starting background task")
    logger.info("Finished background task")

@shared_task
def test_celery_task():
    print("Celery is working")
    return "task complete"