import os
from flask import Flask, session
from flask_session import Session
from redis import Redis

# Create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY'),
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    #SESSION_COOKIE_NAME=os.environ.get('SESSION_COOKIE_NAME'),        
    #SESSION_COOKIE_DOMAN=os.environ.get('SESSION_COOKIE_DOMAN'),
    #SESSION_COOKIE_PATH=os.environ.get('SESSION_COOKIE_PATH'),
    #SESSION_COOKIE_HTTPONLY=os.environ.get('SESSION_COOKIE_HTTPONLY'),
)

SESSION_TYPE = os.environ.get('SESSION_TYPE')
_REDIS_HOST = os.environ.get('REDIS_HOST')
_REDIS_PORT = os.environ.get('REDIS_PORT')
SESSION_REDIS = Redis(host=_REDIS_HOST, port=_REDIS_PORT)
app.config.update(SECRET_KEY=os.urandom(24))
# Start the server side session
app.config.from_object(__name__)
Session(app)



#def create_app(test_config=None):
    
# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/hello')
def home():
    return "Hello!"


from . import db
db.init_app(app)

from . import auth
app.register_blueprint(auth.bp)

from . import accesstokens
app.register_blueprint(accesstokens.bp)
app.add_url_rule('/', endpoint='accesstokens.index')

#    return app


