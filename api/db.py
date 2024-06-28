
import mysql.connector
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host='db',
            port='3306',
            user='root', 
            password='1234', 
            database='finance' 
        )
    return g.db

def init_db():
    db = get_db()
    cursor = db.cursor()
    try:
        with current_app.open_resource('schema.sql', mode='r') as f:
            sql_commands = f.read().split(';')
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
