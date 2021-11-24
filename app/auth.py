import functools
import os
import requests
import json

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app import logger
from app.db import get_conn
from psycopg2.extras import RealDictCursor
import socket
hostname = socket.gethostname()
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_conn()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            with db.cursor() as curs:
                curs.execute(
                "SELECT id FROM soc.user WHERE username = '{}'".format(username)
                )
                if curs.rowcount != 0:
                    error = f"User {username} is already registered."

        if error is None:
            with db.cursor() as curs:
                
                curs.execute(
                    "INSERT INTO soc.user (username, password) VALUES ('{}','{}')".format(username, generate_password_hash(password))
                )
                db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', hostname=hostname)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    app.logger("Login endpoint called")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error, r = lfUserLogin(username, password)
        if error is None:
            session.clear()
            userData = json.loads(r.text)
            session['user_id'] = userData['id']
            session['user_name'] = "{} {}".format(userData['first_name'], userData['last_name'] )
            session['user_email'] = userData['email']
            return redirect(url_for('accesstokens.index'))

        flash(error,'login_error')


    return render_template('auth/login.html', hostname=hostname)

def lfUserLogin(username, password):
    r = apiPass = os.environ.get('API_PASSWORD')
    apiUser = os.environ.get('API_USERNAME')
    loginData = {
            "credentials": {
                "username": username,
                "password": password,
                "field": "email"
            }
        }

    url = 'https://foreninglet.dk/api/memberlogin?version=1'
    error = None
    try:
        r = requests.post(url,auth=(apiUser, apiPass), json=loginData)
        if r.status_code != 200:
            data = json.loads(r.text)
            error = 'Incorrect username or password.'
    except requests.exceptions.RequestException as e:
        raise(SystemExit(e))
    return error,r

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        apiPass = os.environ.get('API_PASSWORD')
        apiUser = os.environ.get('API_USERNAME')
        if not apiPass or not apiUser:
            raise("Missing API Credentials") 
        url = 'https://foreninglet.dk/api/members?version=1'
        try:
            r = requests.get(url,auth=(apiUser, apiPass))
            users = json.loads(r.text)
            for user in users:
                if user['MemberId'] == user_id:
                    g.user = user
                    break
        except requests.exceptions.RequestException as e:
            raise(SystemExit(e))
        #db = get_conn()

        #with db.cursor() as cur:
        #    cur.execute("SELECT * FROM soc.user WHERE id = '{}'".format(user_id))
        #    g.user = cur.fetchone()[0]

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('accesstokens.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
