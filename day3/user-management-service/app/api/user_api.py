from flask import request
from flask_restful import Resource
from ..models.user import User
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import user_db

class UserApi(Resource):

	def get(self, id):
		conn = get_db_connection()
		user = user_db.get_user_details(conn, id)
		close_db_connection(conn)
		return user

	def put(self, id):
		conn = get_db_connection()
		user_db.update_user_details(conn, id, User.from_json(request.json))
		users = user_db.get_user_details(conn, id)
		commit_and_close_db_connection(conn)
		return users

	def delete(self, id):
		conn = get_db_connection()
		user = user_db.get_user_details(conn, id)
		user_db.delete_user(conn, id)
		commit_and_close_db_connection(conn)
		return {'message': f'User [{user["name"]}] deleted from the database'}