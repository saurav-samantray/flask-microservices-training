
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
class AuthApi(Resource):
    def post(self):
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        if email != "test@gmail.com" or password != "test":
            return {"msg": "Bad email or password"}, 401

        access_token = create_access_token(identity=email)
        return {"access_token":access_token}

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
class ProtectedApi(Resource):
    decorators = [jwt_required()]
    def get(self):
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        return {"logged_in_as": current_user}