from datetime import date
import datetime
import os
import redis
from flask import Flask, session
from flask_session import Session
from dotenv import load_dotenv
load_dotenv()
# Create and configure the app
app = Flask(__name__ )#, instance_relative_config=True)
app.secret_key = b'3!K2lhkTbjPYda%ct#b9'
#app.secret_key = os.environ.get('SECRET_KEY')
#REDIS_PORT = os.environ.get('REDIS_PORT') # '6379'
#REDIS_URL = os.environ.get('REDIS_URL')

#SESSION_REDIS = redis.from_url(REDIS_URL)
#SESSION_TYPE = os.environ.get('SESSION_TYPE') #'redis'
#app.config.from_object(__name__)
app.config['SESSION_TYPE'] = os.environ.get('SESSION_TYPE','redis')
app.config['SESSION_PERMANENT'] = True
#app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL','redis://localhost:6379'))
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE')
app.config['SESSION_COOKIE_HTTPONLY'] = os.environ.get('SESSION_COOKIE_HTTPONLY')
app.config['SESSION_COOKIE_DOMAIN'] = os.environ.get('COOKIE_DOMAIN','127.0.0.1')
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_NAME'] = os.getenv('SESSION_COOKIE_NAME','lf-admin-dev')
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=6)
# Start the server side session
Session(app)
from . import db
db.init_app(app)

from . import auth
app.register_blueprint(auth.bp)

from . import accesstokens
app.register_blueprint(accesstokens.bp)
from . import member
app.register_blueprint(member.bp)
app.add_url_rule('/', endpoint='accesstokens.index')

# Let's make sessions permanent, if site is visited every 5 days
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(days=5)

#    return app


