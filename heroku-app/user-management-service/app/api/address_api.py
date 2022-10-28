from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..schemas.address_schema import AddressSchema
from ..exceptions import AddressNotFoundException, InvalidAddressPayload
from ..models.address import Address
from app import restful_api, db

address_schema = AddressSchema()

class AddressApi(Resource):
	decorators = [jwt_required()]
	def get(self, user_id, id):
		address = Address.query.filter_by(user_id=user_id, id=id).first()
		return address.to_json()

	def put(self, user_id, id):
		errors = address_schema.validate(request.json)
		print("errors: "+str(errors))
		if errors:
			raise InvalidAddressPayload(errors, 400)
		address = Address.query.filter_by(user_id=user_id, id=id).first()
		if not address:
			raise AddressNotFoundException(f'Address with ID [{id}] for user [{user_id}]not found in DB')
		updated_address = Address.from_json(request.json)
		address.address_line_1 = updated_address.address_line_1
		address.city = updated_address.city
		address.state = updated_address.state
		address.pin = updated_address.pin
		db.session.commit()
		return address.to_json()

	def delete(self, user_id, id):
		address = Address.query.filter_by(user_id=user_id, id=id).first()
		if not address:
			raise AddressNotFoundException(f'Address with ID [{id}] for user [{user_id}]not found in DB')
		db.session.delete(address)
		db.session.commit()
		return {'message': f'Address [{id}] deleted from user [{user_id}] from the database'}

restful_api.add_resource(AddressApi, '/api/users/<int:user_id>/addresses/<int:id>')