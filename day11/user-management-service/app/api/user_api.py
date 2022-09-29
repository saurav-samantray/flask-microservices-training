from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..models.user import User
from ..database import user_db
from app import restful_api, db, flask_bcrypt
from app.exceptions import UserNotFoundException, InvalidUserPayload
from ..decorators.security import admin_or_self_required
from ..schemas.user_schema import UserSchema

user_schema = UserSchema()

class UserApi(Resource):
	decorators = [jwt_required(), admin_or_self_required()]
	def get(self, id):
		user = User.query.get(id)
		if not user:
			raise UserNotFoundException(f"User with ID [{id}] not found in DB")
		return user.to_json()

	def put(self, id):
		user = User.query.get(id)
		if not user:
			raise UserNotFoundException(f"User with ID [{id}] not found in DB")
		errors = user_schema.validate(request.json)
		if errors:
			raise InvalidUserPayload(errors, 400)
		updated_user = User.from_json(request.json)
		user.name = updated_user.name
		user.email = updated_user.email
		user.age = updated_user.age
		user.password = flask_bcrypt.generate_password_hash(updated_user.password).decode('utf-8')
		db.session.commit()
		return user.to_json()

	def delete(self, id):
		user = User.query.get(id)
		db.session.delete(user)
		db.session.commit()
		return {'message': f'User [{user.email}] deleted from the database'}

restful_api.add_resource(UserApi, '/api/users/<int:id>')