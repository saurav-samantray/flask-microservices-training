from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models.user import User
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import user_db
from ..schemas.user_schema import UserSchema
from ..exceptions import InvalidUserPayload, UserExistsException
from app import restful_api
#from app import flask_bcrypt

user_schema = UserSchema()

class UsersApi(Resource):
	decorators = [jwt_required()]
	def get(self):
		conn = get_db_connection()
		users = user_db.get_users(conn)
		close_db_connection(conn)
		return users

	def post(self):
		errors = user_schema.validate(request.json)
		if errors:
			raise InvalidUserPayload(errors, 400)
		conn = get_db_connection()
		existing_user = user_db.get_user_details_from_email(conn, request.json.get('email'))
		if(existing_user is not None):
			raise UserExistsException(f"User [{request.json.get('email')}] already exists")
		user_db.create_users(conn, User.from_json(request.json))
		users = user_db.get_users(conn)
		commit_and_close_db_connection(conn)
		return users, 201

	def put(self):
		return {'message': 'Hello PUT'}

	def delete(self):
		user_db.delete_all_users()
		return {'message': 'All users deleted'}

restful_api.add_resource(UsersApi, '/api/users')