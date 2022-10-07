from flask import request, jsonify	
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models.user import User
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import user_db
from ..schemas.user_schema import UserSchema
from ..exceptions import InvalidUserPayload, UserExistsException
from app import restful_api, flask_bcrypt, app, db
from ..decorators.security import admin_required
from ..utils import create_admin_user

user_schema = UserSchema()

class UsersApi(Resource):
	decorators = [jwt_required(), admin_required()]
	def get(self):
		return [user.to_json() for user in User.query.all()]

	def post(self):
		errors = user_schema.validate(request.json)
		if errors:
			raise InvalidUserPayload(errors, 400)
		existing_user = User.query.filter_by(email=request.json.get('email')).first()
		if(existing_user is not None):
			raise UserExistsException(f"User [{existing_user.email}] already exists")
		user = User.from_json(request.json)
		user.password = flask_bcrypt.generate_password_hash(user.password).decode('utf-8')
		db.session.add(user)
		db.session.commit()
		new_user = User.query.filter_by(email=user.email).first()
		#user_db.create_user(conn, user)
		#users = user_db.get_users(conn)
		#commit_and_close_db_connection(conn)
		return new_user.to_json(), 201

	def put(self):
		return {'message': 'Hello PUT'}

	def delete(self):
		#user_db.delete_all_users()
		return {'message': 'All users deleted'}

restful_api.add_resource(UsersApi, '/api/users')

@app.before_first_request
def before_first_request():
	print("before_first_request")
	db.create_all()
	initial_admin_user = User.from_json({
		'name': 'Admin User',
		'email': app.config['UMS_ADMIN_EMAIL'], 
		'password': app.config['UMS_ADMIN_PASSWORD'],
		'role': 'ADMIN',
		'age': 45
		})
	create_admin_user(flask_bcrypt, db, initial_admin_user)  