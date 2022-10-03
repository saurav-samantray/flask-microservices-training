from app import jwt

# Set a callback function to return a custom response whenever an expired
# token attempts to access a protected route. This particular callback function
# takes the jwt_header and jwt_payload as arguments, and must return a Flask
# response. Check the API documentation to see the required argument and return
# values for other callback functions.
@jwt.expired_token_loader
def custom_expired_token_callback(jwt_header, jwt_payload):
    return {'message': "Your token has expired. Refresh the token to continue"}, 401

@jwt.unauthorized_loader
def custom_unauthorized_loader(message):
    return {'message': 'Add Authorization details to the header'}, 401    