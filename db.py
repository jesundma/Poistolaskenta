import sqlite3
from flask import g

DATABASE = "database.db"

def get_connection():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.row_factory = sqlite3.Row
    return g.db

def close_connection(exception = None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid


def last_insert_id():
    return getattr(g, "last_insert_id", None)

def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    return result

def init_db():
    con = get_connection()
    with open("schema.sql", "r") as f:
        sql = f.read()
    con.executescript(sql)
    con.commit()

def init_app(app):
    app.teardown_appcontext(close_connection)