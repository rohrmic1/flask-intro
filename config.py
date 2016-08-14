import os


# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'my precious'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    #print (SQLALCHEMY_DATABASE_URI)


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False