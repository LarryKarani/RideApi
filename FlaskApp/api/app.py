from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from ..config import config
from .routes import Home, AllRides, GetRide,  JoinRequest, Register, Login, Usersg


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    jwt = JWTManager(app)
    api = Api(app)
    
    api.add_resource(Home, '/')
    api.add_resource(Register, '/api/v1/regester')
    api.add_resource(Login, '/api/v1/login')
    api.add_resource(AllRides, '/api/v1/rides')
    api.add_resource(GetRide, '/api/v1/rides/<rideId>')
    api.add_resource( JoinRequest, '/api/v1/rides/<rideId>/requests')
    api.add_resource(Usersg, '/api/v1/users')
    
    return app


