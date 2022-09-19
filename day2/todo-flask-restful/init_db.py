import sqlite3

connection = sqlite3.connect('todo.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO todos (name, status) VALUES (?, ?)",
            ('File ITR', 'STARTED')
            )

cur.execute("INSERT INTO todos (name, status) VALUES (?, ?)",
            ('Complete Flask microservices', 'NEW')
            )

connection.commit()
connection.close()