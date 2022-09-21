from flask import request
from flask_restful import Resource
from ..database import get_db_connection, close_db_connection, commit_and_close_db_connection
from ..database import address_db
from ..schemas.address_schema import AddressSchema
from ..exceptions import InvalidAddressPayload
from ..models.address import Address
from app import restful_api

address_schema = AddressSchema()

class AddressApi(Resource):

	def get(self, id):
		conn = get_db_connection()
		addresses = address_db.get_addresses(conn)
		close_db_connection(conn)
		return addresses

	def put(self, id):
		conn = get_db_connection()
		address_db.get_address_details(conn, id) #validate is user exists befire udpate
		address_db.update_address_details(conn, id, Address.from_json(request.json))
		addresses = address_db.get_user_details(conn, id)
		commit_and_close_db_connection(conn)
		return addresses

	def delete(self, id):
		conn = get_db_connection()
		address = address_db.get_address_details(conn, id)
		address_db.delete_address(conn, id)
		commit_and_close_db_connection(conn)
		return {'message': f'Address [{address["id"]}] deleted from the database'}

restful_api.add_resource(AddressApi, '/api/addresses/<int:id>')