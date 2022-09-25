from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import address_db
from ..schemas.address_schema import AddressSchema
from ..exceptions import InvalidAddressPayload
from ..models.address import Address
from app import restful_api

address_schema = AddressSchema()

class AddressesApi(Resource):
	decorators = [jwt_required()]
	def get(self, user_id):
		conn = get_db_connection()
		addresses = address_db.get_addresses(conn, user_id)
		close_db_connection(conn)
		return addresses

	def post(self, user_id):
		errors = address_schema.validate(request.json)
		print("errors: "+str(errors))
		if errors:
			raise InvalidAddressPayload(errors, 400)
		conn = get_db_connection()
		address_db.create_address(conn, Address.from_json(request.json), user_id)
		addresses = address_db.get_addresses(conn, user_id)
		commit_and_close_db_connection(conn)
		return addresses, 201

	def put(self):
		return {'message': 'Hello PUT'}

	def delete(self):
		return {'message': 'Hello DELETE'}

restful_api.add_resource(AddressesApi, '/api/users/<int:user_id>/addresses')		