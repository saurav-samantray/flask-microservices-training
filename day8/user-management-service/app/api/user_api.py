from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models.user import User
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import user_db
from app import restful_api
from app.exceptions import UserNotFoundException
from ..decorators.security import admin_or_self_required

class UserApi(Resource):
	decorators = [jwt_required(), admin_or_self_required()]
	def get(self, id):
		conn = get_db_connection()
		user = user_db.get_user_details(conn, id)
		close_db_connection(conn)
		return user

	def put(self, id):
		conn = get_db_connection()
		user_db.get_user_details(conn, id) #validate is user exists befire udpate
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

restful_api.add_resource(UserApi, '/api/users/<int:id>')