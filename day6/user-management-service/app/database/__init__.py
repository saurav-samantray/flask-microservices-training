import sqlite3

def get_db_connection():
    conn = sqlite3.connect('user-management.db')
    conn.row_factory = sqlite3.Row
    return conn


def close_db_connection(conn):
    conn.close()

def commit_and_close_db_connection(conn):
    conn.commit()
    conn.close()