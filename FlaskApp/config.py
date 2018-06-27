import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
	DEBUG = False


class StaginConfig(Config):
	DEBUG = False

config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'staging': StaginConfig
}
