import sqlite3
import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext
from os import environ

def get_conn():
    if 'conn' not in g:
        #dbUser = environ.get("DB_USER")
        #dbPass = environ.get("DB_PASS")
        #dbHost = environ.get("DB_HOST","cockroachdb-public")
        #dbName = "lfadmin"
        #DATABASE_URL = "postgresql://{}@{}:26257/{}?sslmode=disable".format(dbUser, dbHost, dbName)
        DATABASE_URL = environ.get('DATABASE_URL')
        g.conn = psycopg2.connect(DATABASE_URL)

    return g.conn


def close_db(e=None):
    g.conn.close()

def init_db():
    conn = get_conn()

    with conn:
        with conn.cursor() as curs:
            with current_app.open_resource('schema.sql') as f:
                curs.execute(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    #app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)