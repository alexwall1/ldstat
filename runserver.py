from ldstat import app
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter


if __name__ == '__main__':
    handler = RotatingFileHandler('ldstat.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s ''[in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(handler)
    app.run()