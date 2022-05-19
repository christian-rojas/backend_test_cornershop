from unicodedata import name
from celery import shared_task
from backend_test.celery import app
from food.models import Menu
from datetime import date
# from __future__ import absolute_import

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# @app.task(bind=True)
@app.task(name="send")
def send():
    # menu = Menu()
    # menu.date = date.today()
    # menu.save()
    logger.info('Adding')
