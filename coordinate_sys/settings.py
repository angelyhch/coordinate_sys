import os
import sys


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('auto-mail-sender', MAIL_USERNAME)



class DevelopmentConfig(BaseConfig):

    name = os.getenv('USER')
    password = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    database_name = os.getenv('DATABASE_NAME')

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{name}:{password}@{host}:{port}/{database_name}"

    CACHE_TYPE = 'simple'

class TestConfig(BaseConfig):
    pass


class ProductConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'product': ProductConfig
}
