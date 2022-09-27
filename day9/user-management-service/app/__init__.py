import logging
from flask import Flask
from flask.logging import default_handler
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from .config import load_configuration
from .models.user import User
from .utils import create_admin_user

app = Flask(__name__)
load_configuration(app)

class CustomApi(Api):
    def handle_error(self, e):
        return {'code': e.code, 'message': 'error', 'errors': e.message}, e.code

restful_api = CustomApi(app)

flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.before_first_request
def before_first_request():
    print("before_first_request")
    initial_admin_user = User.from_json({
        'name': 'Admin User',
        'email': app.config['UMS_ADMIN_EMAIL'], 
        'password': app.config['UMS_ADMIN_PASSWORD'],
        'role': 'ADMIN',
        'age': 45
        })
    create_admin_user(flask_bcrypt, initial_admin_user)    


### Logging setting
app.logger.setLevel(logging.INFO)
default_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s %(threadName)s: %(message)s'
))