from flask import Flask
from flask_restful import Resource, Api

from .config import config



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    api = Api(app)

    #regester urls here
    
    return app
