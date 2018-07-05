from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from ..config import config
from .routes import Home, AllRides, GetRide,  JoinRequest, Register, Login, RideOfferResponse
from .db_config import con
from .db import create_table


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    jwt = JWTManager(app)
    api = Api(app)

    #create table queries
    user_table_queries=  'CREATE TABLE IF NOT EXISTS users (Id SERIAL PRIMARY KEY, username VARCHAR(255),\
                      password VARCHAR(255), email VARCHAR(255));'

    ride_offer_queries= 'CREATE TABLE IF NOT EXISTS rides(Id SERIAL PRIMARY KEY, current_location VARCHAR(255),\
                     destination VARCHAR(255), depature_time VARCHAR(255), seats_available VARCHAR(255),\
                     user_id SERIAL, FOREIGN KEY (user_id) REFERENCES users(Id), cost INTEGER);'

    request_queries =   'CREATE TABLE IF NOT EXISTS request(Id SERIAL PRIMARY KEY, Username VARCHAR(255),\
                      current_location VARCHAR(255), destination VARCHAR(255) , depature_time VARCHAR(255),\
                      request_id SERIAL, FOREIGN KEY(request_id) REFERENCES rides (Id));'

    ride_offer_response_queries = 'CREATE TABLE IF NOT EXISTS response(Id SERIAL PRIMARY KEY,\
                      request_id SERIAL, rideoffer_id SERIAL, user_id SERIAL, reply VARCHAR(255),\
                       FOREIGN KEY(rideoffer_id) REFERENCES rides (Id),\
                        FOREIGN KEY(request_id) REFERENCES request (Id),\
                        FOREIGN KEY(user_id) REFERENCES users(Id));'


    create_table(con, user_table_queries)
    create_table(con, ride_offer_queries)
    create_table(con, request_queries)
    create_table(con, ride_offer_response_queries)

    api.add_resource(Home, '/')
    api.add_resource(Register, '/api/v1/auth/signup')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(AllRides, '/api/v1/rides')
    api.add_resource(GetRide, '/api/v1/rides/<rideId>')
    api.add_resource( JoinRequest, '/api/v1/rides/<rideId>/requests')
    api.add_resource(RideOfferResponse,  '/api/v1/users/rides/<rideId>/requests/<requestId>')

    return app
    