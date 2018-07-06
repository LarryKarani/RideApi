from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from ..config import config
from .routes import AllRides, GetRide,  JoinRequest, Register, Login, RideOfferResponse
from .db_config import con
from .db import create_table


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    jwt = JWTManager(app)
    api = Api(app)

    #create table queries
    create_table()


    api.add_resource(Register, '/api/v1/auth/signup')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(AllRides, '/api/v1/rides')
    api.add_resource(GetRide, '/api/v1/rides/<rideId>')
    api.add_resource( JoinRequest, '/api/v1/rides/<rideId>/requests')
    api.add_resource(RideOfferResponse,  '/api/v1/users/rides/<rideId>/requests/<requestId>')

    return app
    