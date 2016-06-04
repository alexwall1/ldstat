__author__ = 'alwa'

from flask.ext.script import Manager
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from ldstat import app
from ldstat.batch import get_posts as _get_post
from ldstat.batch import update_posts as _update_posts

manager = Manager(app)

@manager.command
def get_posts():
    app.logger.info("started retrieving posts")
    _get_post()
    app.logger.info("finished retrieving posts")

@manager.command
def update_posts(batch):
    app.logger.info("started updating posts")
    _update_posts(batch)
    app.logger.info("finished updating posts")

if __name__ == "__main__":
    handler = RotatingFileHandler('manage.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s ''[in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(handler)
    manager.run()