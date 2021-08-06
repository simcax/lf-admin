import functools


from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_conn()
        error = None
        with db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM soc.user WHERE username = '{}'".format(username)
            )
            user = cur.fetchone()

        if cur.rowcount == 0:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('accesstokens.index'))

        flash(error)

    return render_template('auth/login.html', hostname=hostname)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_conn()

        with db.cursor() as cur:
            cur.execute("SELECT * FROM soc.user WHERE id = '{}'".format(user_id))
            g.user = cur.fetchone()[0]

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