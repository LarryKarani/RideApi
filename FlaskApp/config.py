import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
class DevelopmentConfig(Config):
    DEBUG = True
    os.environ["DATABASE_NAME"] = "ridemyway"

class TestingConfig(Config):
    TESTING = True
    os.environ["DATABASE_NAME"] = "tester"

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