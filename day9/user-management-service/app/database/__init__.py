import sqlite3
from flask import current_app

def get_db_connection():
    conn = sqlite3.connect(current_app.config['DATABASE_URI'])
    conn.row_factory = sqlite3.Row
    return conn


def close_db_connection(conn):
    conn.close()

def commit_and_close_db_connection(conn):
    conn.commit()
    conn.close()