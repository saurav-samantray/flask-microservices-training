from functools import wraps

from flask import request
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt
)

# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == 'ADMIN':
                return fn(*args, **kwargs)
            else:
                return {'msg': "Admins only!"}, 403

        return decorator

    return wrapper


# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator or is performing action on self
def admin_or_self_required(user_id_param='id'):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            request_user_id = request.view_args.get(user_id_param)
            print(f"Evaluating for request id [{request_user_id}]")
            if claims["role"] == 'ADMIN' or (request_user_id is not None and request_user_id == claims["user_id"]):
                return fn(*args, **kwargs)
            else:
                return {'msg': "Admins only!"}, 403

        return decorator

    return wrapper