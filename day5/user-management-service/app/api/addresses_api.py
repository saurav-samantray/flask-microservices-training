from flask_restful import Resource

class AddressesApi(Resource):

	def get(self):
		return {'message': 'Hello GET'}

	def post(self):
		return {'message': 'Hello POST'}, 201

	def put(self):
		return {'message': 'Hello PUT'}

	def delete(self):
		return {'message': 'Hello DELETE'}