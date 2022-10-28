import os
import datetime

_deployed_env_ = os.environ.get("FLASK_ENV", default=None)
print(f"Environment: [{_deployed_env_}]")


class Config(object):
    TESTING = False
    JWT_SECRET_KEY = 'this-is-a-complicated-secret'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=1)
    UMS_ADMIN_EMAIL = 'saurav@gmail.com'
    UMS_ADMIN_PASSWORD = 'saurav'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/user-management.db'

class ProductionConfig(Config):
    DATABASE_URI = 'sqlite:////tmp/user-management-prod.db'

class DevelopmentConfig(Config):
    DATABASE_URI = 'sqlite:////tmp/user-management-dev.db'
    
    DEBUG = True

class TestingConfig(Config):
    DATABASE_URI = 'sqlite:////tmp/user-management-test.db'
    TESTING = True

def load_configuration(app):
    print(_deployed_env_)
    if (_deployed_env_ == None):
        app.config.from_object(DevelopmentConfig)
    elif (_deployed_env_ == 'dev'):
        app.config.from_object(DevelopmentConfig)
    elif (_deployed_env_ == 'testing'):
        app.config.from_object(TestingConfig)
    elif (_deployed_env_ == 'production'):
        app.config.from_object(ProductionConfig)
    else:
        raise RuntimeError('Unknown environment setting provided.')    