import os
import sqlite3

import click
from flask import g, current_app
from werkzeug.security import generate_password_hash

__folder = ''
__filename = 'app.sqlite'
__path = 'app.sqlite'


def init_app(app):
    global __folder, __filename, __path

    __folder = app.config.get('DATA_FOLDER') or app.instance_path
    __filename = app.config.get('DATA_FILENAME') or 'app.sqlite'
    __path = os.path.join(__folder, __filename)

    app.cli.add_command(__install_command)
    app.cli.add_command(__reset_admin_command)
    app.before_request(__on_before_request)
    app.teardown_appcontext(__on_teardown_appcontext)


def get_connection():
    def dict_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    db = sqlite3.connect(
        __path,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = dict_factory

    return db


def execute(query, args=(), db=None):
    db = db or g.db

    lastrowid = db.execute(query, args).lastrowid
    db.commit()

    return lastrowid


def fetchone(query, args=(), db=None):
    db = db or g.db

    return db.execute(query, args).fetchone()


def fetchall(query, args=(), db=None):
    db = db or g.db

    return db.execute(query, args).fetchall()


def install():
    os.makedirs(__folder, exist_ok=True)

    with get_connection() as db:
        with current_app.open_resource('schema.sql') as file:
            db.executescript(file.read().decode('utf8'))
            db.commit()

        __reset_admin(db)


def reset_admin():
    with get_connection() as db:
        __reset_admin(db)


def __reset_admin(db):
    query = '''
            SELECT "id"
            FROM "user"
            WHERE "username" = 'admin';
    '''

    user_id = (fetchone(query, db=db) or {'id': None})['id']
    digest = generate_password_hash('Admin123.')

    if user_id:
        query = '''
                UPDATE "user"
                SET "username" = ?,
                    "password" = ?,
                    "role"     = ?
                WHERE "id" = ?;
        '''
        args = ('admin', digest, 'admin', user_id)
    else:
        query = '''
                INSERT INTO "user"
                    ("username", "password", "role")
                VALUES (?, ?, ?);
        '''
        args = ('admin', digest, 'admin')

    execute(query, args, db=db)


@click.command('install')
def __install_command():
    install()
    click.echo('Application installation successful.')


@click.command('reset-admin')
def __reset_admin_command():
    reset_admin()
    click.echo('Admin reset successful.')


def __on_before_request():
    if 'db' not in g:
        g.db = get_connection()


def __on_teardown_appcontext(e):
    if 'db' in g:
        g.pop('db').close()


from persistence.model.user import User
from persistence.repository.recipe import RecipeRepository
from persistence.repository.user import UserRepository
