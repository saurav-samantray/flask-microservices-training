import logging
from flask import Flask
from flask.logging import default_handler
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

### Logging setting
app.logger.setLevel(logging.INFO)
default_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s %(threadName)s: %(message)s'
))


## Imports are essential for python interpreter to find the model files for migration
from .models import user, address