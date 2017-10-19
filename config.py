import os


class ProductionConfig(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pay_trio_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DeveloperConfig(ProductionConfig):
    ASSETS_DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG = True
