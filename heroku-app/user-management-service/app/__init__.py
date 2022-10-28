from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from .config import load_configuration

app = Flask(__name__)
load_configuration(app)

class CustomApi(Api):
    def handle_error(self, e):
        return {'code': e.code, 'message': 'error', 'errors': e.message}, e.code
restful_api = CustomApi(app)

flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)  

@app.route("/")
def index():
    return "Hello From User Management Service! Saurav Samantray"


## Imports are essential for python interpreter to find the model files for migration
from .models import user, address