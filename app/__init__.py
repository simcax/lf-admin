import os
from flask import Flask, session
from flask_session import Session
from logging.config import dictConfig
# Create and configure the app
app = Flask(__name__, instance_relative_config=True)

REDIS_PORT = '6379'
REDIS_HOST = 'localhost'
SESSION_TYPE = 'redis'
app.config.from_object(__name__)

# Start the server side session
Session(app)



  
# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/hello')
def home():
    print(app.config['SECRET_KEY'])
    print(app.config)
    session['test'] = "Hello"
    return "Hello!"


from . import db
db.init_app(app)

from . import auth
app.register_blueprint(auth.bp)

from . import accesstokens
app.register_blueprint(accesstokens.bp)
app.add_url_rule('/', endpoint='accesstokens.index')

#    return app


