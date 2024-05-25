from celery import shared_task
from logging import getLogger

logger = getLogger(__name__)


@shared_task
def debug_task(self):
    logger.info("Request: {0!r}".format(self.request))
