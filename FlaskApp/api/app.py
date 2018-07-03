from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from ..config import config
from .routes import Home, AllRides, GetRide,  JoinRequest, Register, Login, Usersg
from .db_config import con
from .db import create_table



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    jwt = JWTManager(app)
    api = Api(app)

    #create table queries
    user_table_queries=  'CREATE TABLE IF NOT EXISTS "user"(Id SERIAL PRIMARY KEY, username VARCHAR(85),\
                      password VARCHAR(85), email VARCHAR(25));'

    ride_offer_queries= 'CREATE TABLE IF NOT EXISTS rides(Id SERIAL PRIMARY KEY, current_location VARCHAR(85),\
                     destination VARCHAR(85), depature_time VARCHAR(85), seats_available VARCHAR(85),\
                     user_id SERIAL, FOREIGN KEY (user_id) REFERENCES "user"(Id), cost INTEGER);'

    request_queries =   'CREATE TABLE IF NOT EXISTS request(Id SERIAL PRIMARY KEY, Username VARCHAR(85),\
                      current_location VARCHAR(85), destination VARCHAR(85) , depature_time VARCHAR(85),\
                      request_id SERIAL, FOREIGN KEY(request_id) REFERENCES rides (Id));'



    create_table(con, user_table_queries)
    create_table(con, ride_offer_queries)
    create_table(con, request_queries)


    
    api.add_resource(Home, '/')
    api.add_resource(Register, '/api/v1/regester')
    api.add_resource(Login, '/api/v1/login')
    api.add_resource(AllRides, '/api/v1/rides')
    api.add_resource(GetRide, '/api/v1/rides/<rideId>')
    api.add_resource( JoinRequest, '/api/v1/rides/<rideId>/requests')
    api.add_resource(Usersg, '/api/v1/users')
    
    return app
  


