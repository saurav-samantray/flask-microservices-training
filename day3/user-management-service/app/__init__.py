from flask import Flask
from flask_restful import Api

from .api.users_api import UsersApi
from .api.user_api import UserApi

app = Flask(__name__)
api = Api(app)

api.add_resource(UsersApi, '/api/users')
api.add_resource(UserApi, '/api/users/<int:id>')