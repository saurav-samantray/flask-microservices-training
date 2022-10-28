from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..schemas.address_schema import AddressSchema
from ..exceptions import InvalidAddressPayload
from ..models.address import Address
from app import restful_api, db
from ..decorators.security import admin_or_self_required

address_schema = AddressSchema()

class AddressesApi(Resource):
	decorators = [jwt_required(), admin_or_self_required(user_id_param='user_id')]
	def get(self, user_id):
		addresses = Address.query.filter_by(user_id=user_id).all()
		return [address.to_json() for address in addresses]

	def post(self, user_id):
		errors = address_schema.validate(request.json)
		print("errors: "+str(errors))
		if errors:
			raise InvalidAddressPayload(errors, 400)
		new_address = Address.from_json(request.json)
		new_address.user_id = user_id
		db.session.add(new_address)
		db.session.commit()
		addresses = Address.query.filter_by(user_id=user_id).all()
		return [address.to_json() for address in addresses], 201

	def put(self):
		return {'message': 'Hello PUT'}

	def delete(self):
		return {'message': 'Hello DELETE'}

restful_api.add_resource(AddressesApi, '/api/users/<int:user_id>/addresses')		