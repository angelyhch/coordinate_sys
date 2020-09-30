import os
import sys


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class DevelopmentConfig(BaseConfig):

    name = os.getenv('USER')
    password = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    database_name = os.getenv('DATABASE_NAME')

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{name}:{password}@{host}:{port}/{database_name}"

class TestConfig(BaseConfig):
    pass


class ProductConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'product': ProductConfig
}
