from flask import request
from flask_restful import Resource
from ..models.user import User
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import user_db

class UsersApi(Resource):

	def get(self):
		conn = get_db_connection()
		users = user_db.get_users(conn)
		close_db_connection(conn)
		return users

	def post(self):
		conn = get_db_connection()
		user_db.create_users(conn, User.from_json(request.json))
		users = user_db.get_users(conn)
		commit_and_close_db_connection(conn)
		return users, 201

	def put(self):
		return {'message': 'Hello PUT'}

	def delete(self):
		return {'message': 'Hello DELETE'}