import sqlite3


def initialize(db_name):
    connection = sqlite3.connect(db_name)
    with open('schema.sql') as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()

if __name__ == '__main__':
    initialize('user-management-dev.db')