import os
import redis
from flask import Flask, session
from flask_session import Session
from logging.config import dictConfig
# Create and configure the app
app = Flask(__name__, instance_relative_config=True)

#REDIS_PORT = os.environ.get('REDIS_PORT') # '6379'
REDIS_URL = os.environ.get('REDIS_URL')

SESSION_REDIS = redis.from_url(REDIS_URL)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)

# Start the server side session
Session(app)

from . import db
db.init_app(app)

from . import auth
app.register_blueprint(auth.bp)

from . import accesstokens
app.register_blueprint(accesstokens.bp)
app.add_url_rule('/', endpoint='accesstokens.index')

#    return app


