from flask import Flask
from database import init_db, db_session

app = Flask(__name__)
app.config.from_object('ldstat.config')

init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


from ldstat import views