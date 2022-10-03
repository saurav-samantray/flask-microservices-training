from app import app, db
from app.api.users_search_api import UsersSearchApi
from app.api.users_api import UsersApi
from app.api.user_api import UserApi
from app.api.addresses_api import AddressesApi
from app.api.address_api import AddressApi
from app.api.auth_api import AuthApi, RegisterApi
from app.callbacks import jwt_callbacks

if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0")