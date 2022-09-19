from app import app, api
from app.api.users_api import UsersApi
from app.api.user_api import UserApi

if __name__ == '__main__':
    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/users/<int:id>')
    app.run()