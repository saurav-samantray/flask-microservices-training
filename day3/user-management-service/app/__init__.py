from flask import Flask
from flask_restful import Api
from .config import load_configuration


from .api.users_api import UsersApi
from .api.user_api import UserApi

app = Flask(__name__)
load_configuration(app)

class CustomApi(Api):
    def handle_error(self, e):
        return {'code': e.code, 'message': 'error', 'errors': e.message}, e.code
api = CustomApi(app)

api.add_resource(UsersApi, '/api/users')
api.add_resource(UserApi, '/api/users/<int:id>')