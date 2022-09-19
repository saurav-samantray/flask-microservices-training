import json
from flask import Flask, request
from flask_restful import Resource, Api
import sqlite3
from exceptions import ToDoAlreadyExists, ToDoDoesnNotExists


app = Flask(__name__)
class CustomApi(Api):
    def handle_error(self, e):
        return {'code': e.code, 'message': e.message}, 400

api = CustomApi(app)

def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row #to make each row return dict instead of tuple
    return conn

def get_todos(conn):
    results = conn.execute('SELECT id, name, status, created FROM todos').fetchall()
    results = [dict(row) for row in results]
    return results

def create_todos(conn, todo):
    conn.execute('INSERT INTO todos(name, status) VALUES (?, ?)',(todo['name'], todo['status']))
    conn.commit()
    return get_todos(conn)

def update_todos(conn, todo):
    conn.execute('UPDATE todos SET name = ?, status = ? WHERE id = ?',(todo['name'], todo['status'], todo['id']))
    conn.commit()
    return get_todos(conn)

def delete_todos(conn, id):
    conn.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    return get_todos(conn)	

class ToDo(Resource):

	def get(self):
		conn = get_db_connection()
		todos = get_todos(conn)
		conn.close()
		return todos

	def post(self):
		conn = get_db_connection()
		todos = get_todos(conn)
		todo = request.json
		for td in todos:
			if td['name'] == todo['name']:
				raise ToDoAlreadyExists(f"Todo [{todo['name']}] already exits", 400)
		todos = create_todos(conn, todo)
		conn.close()       
		return todos, 201

	def put(self):
		conn = get_db_connection()
		todos = get_todos(conn)
		todo = request.json
		ids = [td['id'] for td in todos]
		if todo['id'] not in ids:
			raise ToDoDoesnNotExists(f"Todo with ID [{todo['id']}] doesn't exits", 400)
		todos = update_todos(conn, todo)
		conn.close()       
		return todos

	def delete(self):
		conn = get_db_connection()
		todos = get_todos(conn)
		id_to_delete = request.args['id']
		ids = [str(td['id']) for td in todos]
		if id_to_delete not in ids:
			raise ToDoDoesnNotExists(f"Todo with ID [{id_to_delete}] doesn't exits", 400)
		todos = delete_todos(conn, id_to_delete)
		conn.close()       
		return todos

api.add_resource(ToDo, '/api/todos')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)