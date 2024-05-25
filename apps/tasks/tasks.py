from celery import shared_task
from logging import getLogger

logger = getLogger(__name__)


@shared_task
def debug_task(self):
    logger.info("Request: %s", self.request)
