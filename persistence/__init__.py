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

    app.before_request(__connect)
    app.cli.add_command(__install_command)
    app.cli.add_command(__reset_admin_command)
    app.teardown_appcontext(__disconnect)


@click.command('install')
def __install_command():
    __install()
    __reset_admin()

    click.echo('Application installation successful.')


@click.command('reset-admin')
def __reset_admin_command():
    __reset_admin()

    click.echo('Admin reset successful.')


def __install():
    os.makedirs(__folder, exist_ok=True)

    db = sqlite3.connect(
        __path,
        detect_types=sqlite3.PARSE_DECLTYPES
    )

    with db:
        db.row_factory = __dict_factory

        with current_app.open_resource('schema.sql') as file:
            db.executescript(file.read().decode('utf8'))
            db.commit()


def __reset_admin():
    db = sqlite3.connect(
        __path,
        detect_types=sqlite3.PARSE_DECLTYPES
    )

    with db:
        db.row_factory = __dict_factory

        query = '''
                    SELECT "id", "username", "password", "role"
                        FROM "user"
                        WHERE username = 'admin';
                '''
        user = db.execute(query).fetchone()

        digest = generate_password_hash('Admin123.')
        print(digest)

        if user:
            query = '''
                        UPDATE "user" SET
                                "username" = ?,
                                "password" = ?,
                                "role" = ?
                            WHERE "id" = ?;
                    '''
            db.execute(query, ('admin', digest, 'admin', user['id']))
        else:
            query = '''
                        INSERT INTO "user" ("username", "password", "role")
                            VALUES(?, ?, ?);
                    '''
            db.execute(query, ('admin', digest, 'admin'))

        db.commit()


def __connect():
    if 'db' not in g:
        g.db = sqlite3.connect(
            __path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = __dict_factory


def __disconnect(e):
    db = g.pop('db', None)

    if db:
        db.close()


def __dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


from persistence.model.user import User
from persistence.repository.recipe import RecipeRepository
from persistence.repository.user import UserRepository
