__author__ = 'alwa'

from flask import Flask
from celery_factory import make_celery
from database import init_db

app = Flask(__name__)
app.config.from_object('ldstat.config')
init_db()

from ldstat.models import Batch
from ldstat.batch import get_objects, get_municipalities, get_professional_groups, get_posts, update_posts

celery = make_celery(app)

import logging
from logging.handlers import RotatingFileHandler
from celery.utils.log import get_task_logger

handler = RotatingFileHandler('tasks.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
logger = get_task_logger(__name__)


@celery.task()
def async_professional_areas(cls):
    get_objects(cls)


@celery.task()
def async_municipalities():
    get_municipalities()


@celery.task()
def async_professional_groups():
    get_professional_groups()


@celery.task()
def async_posts():
    get_posts()


@celery.task()
def async_update_posts():
    # update the latest complete batch
    batch = Batch.query.filter_by(complete=True).order_by(Batch.id).one()
    logger.info('Updating posts in batch %s' % batch.id)
    update_posts(batch.id)
