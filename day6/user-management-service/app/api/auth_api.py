
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from ..models.user import User
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import user_db
from ..database.user_db import get_user_details_from_email
from ..schemas.user_schema import UserSchema
from ..exceptions import InvalidUserPayload
from app import flask_bcrypt
user_schema = UserSchema()

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
class AuthApi(Resource):
	def post(self):
		email = request.json.get("email", None)
		password = request.json.get("password", None)
		conn = get_db_connection()
		user = get_user_details_from_email(conn, email)
		if email != user.email or not flask_bcrypt.check_password_hash(user.password, password):
			return {"msg": "Bad email or password"}, 401

		access_token = create_access_token(identity=email)
		return {"access_token":access_token}

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
class RegisterApi(Resource):
	def post(self):
		errors = user_schema.validate(request.json)
		print("errors: "+str(errors))
		if errors:
			raise InvalidUserPayload(errors, 400)
		user = User.from_json(request.json)
		user.password = flask_bcrypt.generate_password_hash(user.password).decode('utf-8')
		#user_dict['password'] = flask_bcrypt.generate_password_hash(user_dict['password'])
		conn = get_db_connection()
		user_db.create_users(conn, user)
		users = user_db.get_users(conn)
		commit_and_close_db_connection(conn)
		return users, 201
		