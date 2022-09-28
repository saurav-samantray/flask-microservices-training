
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from ..models.user import User
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import user_db
from ..database.user_db import get_user_details_from_email
from ..schemas.user_schema import UserSchema
from ..exceptions import InvalidUserPayload, UserExistsException, UserNotFoundException
from app import flask_bcrypt, restful_api, db
user_schema = UserSchema()

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
class AuthApi(Resource):
	def post(self):
		email = request.json.get("email", None)
		password = request.json.get("password", None)
		user = User.query.filter_by(email=email).first()
		if user is None:
			raise UserNotFoundException(f"User with email [{email}] not found in DB", 400)
		if email != user.email or not flask_bcrypt.check_password_hash(user.password, password):
			return {"msg": "Bad email or password"}, 401

		# You can use the additional_claims argument to either add
		# custom claims or override default claims in the JWT.
		additional_claims = {"role": user.role, "user_id": user.id}			

		access_token = create_access_token(identity=email, additional_claims=additional_claims)
		refresh_token = create_refresh_token(identity=email)
		return {"access_token":access_token, "refresh_token": refresh_token, "user_id": user.id}


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
class RefreshTokenApi(Resource):
	decorators = [jwt_required(refresh=True)]
	def post(self):
		identity_email = get_jwt_identity()
		user = User.query.filter_by(email=identity_email).first()
		if user is None:
			raise UserNotFoundException(f"User with email [{identity_email}] not found in DB", 400)

		additional_claims = {"role": user.role, "user_id": user.id}	
		access_token = create_access_token(identity=identity_email, additional_claims=additional_claims)
		return {"access_token":access_token}

# User Registration API
# Ability of create your profile with email, password and other relevent fields
class RegisterApi(Resource):
	def post(self):
		user_payload = request.json
		#avoid letting users assign role for themself
		user_payload['role'] = 'USER'
		#Payload Validation
		errors = user_schema.validate(user_payload)
		print("errors: "+str(errors))
		if errors:
			raise InvalidUserPayload(errors, 400)
		#Validating duplicate user
		existing_user = User.query.filter_by(email=request.json.get('email')).first()
		if(existing_user is not None):
			raise UserExistsException(f"User [{existing_user.email}] already exists")
		user = User.from_json(request.json)
		user.password = flask_bcrypt.generate_password_hash(user.password).decode('utf-8')
		db.session.add(user)
		db.session.commit()
		new_user = User.query.filter_by(email=user.email).first()
		return new_user.to_json()

restful_api.add_resource(AuthApi, '/api/auth')
restful_api.add_resource(RegisterApi, '/api/register')
restful_api.add_resource(RefreshTokenApi, '/api/refresh')
		