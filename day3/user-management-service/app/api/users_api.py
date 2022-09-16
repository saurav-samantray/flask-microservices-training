from flask_restful import Resource
from ..models.user import User

userData = [
    User("Saurav", "saurav@gmail.com", 33, "saurav@123").__dict__,
    User("JP", "jp@gmail.com", 26, "jp@123").__dict__,
    User("DJ", "dj@gmail.com", 42, "dj@123").__dict__
    ]

class UsersApi(Resource):

	def get(self):
		return userData

	def post(self):
		return {'message': 'Hello POST'}, 201

	def put(self):
		return {'message': 'Hello PUT'}

	def delete(self):
		return {'message': 'Hello DELETE'}