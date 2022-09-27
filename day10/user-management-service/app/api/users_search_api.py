from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import restful_api, db, app

from ..models.user import User
from ..exceptions import UserNotFoundException

class UsersSearchApi(Resource):
	decorators = [jwt_required(optional=True)]	#Add appropriate decorators
	def get(self):
		email = request.args.get('email')
		if not email:
			return {'message': 'Mandatory parameter email not found in request'}, 400
		user = User.query.filter_by(email=email).first()
		if not user:
			app.logger.error(f"User [{email}] not found in database")
			raise UserNotFoundException(f"User [{email}] doesnot exists in DB")
		
		identity_email = get_jwt_identity()
		if identity_email:
			return user.to_json()
		else:
			return {'name': user.name, 'email': user.email}

# Uncomment the below line by adding a valid url mapping for the user search API
restful_api.add_resource(UsersSearchApi, '/api/users/search')