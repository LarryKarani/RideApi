from flask_jwt_extended import(create_access_token, create_refresh_token, jwt_required,jwt_refresh_token_required,get_jwt_identity,get_raw_jwt)
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
import json


from.user import User
from .utils import Validator
from .rideoffers import RideOffer
from .request import RequestsJ


parser = reqparse.RequestParser()
parser.add_argument('username', help = 'username cannot be blank', required=True)
parser.add_argument('password', help = 'password cannot be blank', required=True)

class Home(Resource):
    def get(self):
        return redirect("https://ridemyway6.docs.apiary.io/", code=302)
class Usersg(Resource):
    """Used to confirm that a user has been added by getting all the users in the Db"""
    def get(self):
        response = jsonify(User.get_all_users())
        response.status_code = 200
        return response 
        
class Login(Resource):
    def post(self):
        
        data = parser.parse_args()
        current_user = User.return_user(data['username'])

        if not current_user:
            return {'message':'User {} does\'t exist'.format(data['username'])}

        if check_password_hash(current_user['password'], data['password'].strip()):
            access_token = create_access_token(identity=data['username'])
            refresh_token =create_refresh_token(identity=data['username'])
            response = jsonify({
                "message":"logged in as {}".format(current_user['username']),
                "acces_token":access_token,
                'refresh_token':refresh_token
                })
    
            response.status_code= 200

            return response
            
        else:
            return {'message':'Wrong credentials'}

class Register(Resource):
    def post(self):
        """"register a new user"""

        data = request.get_json(force=True)
        """pass through the validator method to confirm details"""
        message= Validator(data, 'reg').validate()

        if message:
            response=jsonify(message)
            response.status_code =400

            return response

        """check if email is already registered"""

        if User.return_user(data['email'].strip().lower()):
            response = jsonify({'message': 'Email already registered'})
            response.status_code =400
            return response

        if User.return_user(data['username'].strip()):
            response = jsonify({'message': 'username already registered'})
            response.status_code =400
            return response

        new_user = User(data['name'].strip(), data['username'].strip(), data['email'].strip().lower(),generate_password_hash(data['password'].strip())).register_user()

        message = {
            'user':{
                'name': new_user['name'],
                'username':new_user['username'],
                'email': new_user['email']
            },

            'message': "User created successfully"
        }

        response = jsonify(message)
        response.status_code = 201

        return response



class AllRides(Resource):

    @jwt_required
    def get(self):
        response = jsonify(RideOffer.get_all_rides())
        response.status_code = 200

        return response
    @jwt_required
    def post(self):
        """creates a new ride offer"""
        content = request.get_json(force=True)
        message = Validator(content, 'create_ride').validate()
        
        if message:
            response = jsonify(message)
            response.status_code= 400

            return response

        new_offer = RideOffer(
            content['name'].strip(),content['From'],
            content['To'],content['car_model'],content['cost'],
            content['seats_available'], content['time']
             ).create_ride()
        
        message = {
            'ride':{
                'name': new_offer['name'],
                'from': new_offer['From'],
                'To': new_offer['To'],
                'time': new_offer['time']
            },
            'message':f"ride offer created succesfully on {new_offer['date_created']}"
        }

        response = jsonify(message)
        response.status_code=201

        return response
    
class GetRide(Resource):

    @jwt_required
    def get(self, rideId):
        #retrieves a single ride offer from the list of all rides
        
        offer =  RideOffer.get_specific_offer(rideId)

        if not offer:
            response = jsonify({"message": "ride offer for id provided doesnt exist"})
            response.status_code=400
            return response

        response = jsonify(offer)
        response.status_code = 200
        return response

class JoinRequest(Resource):
    @jwt_required
    def post(self, rideId):
        data = request.get_json(force=True)
        message = Validator(data, 'request_ride').validate()

        if message:
            response = jsonify(message)
            response.status_code = 400

            return response

        ride_to_request = RideOffer.get_specific_offer(rideId)

        if not ride_to_request:
            response = jsonify({'message': 'ride offer does not exist'})
            response.status_code=400

    
        join_request = RequestsJ(data['name'], data['From'], data['To'], data['seats_needed'], data['time'], rideId).request_ride()

        message = {
            'request':'created succesfully',
            'details': join_request
        }  
        response = jsonify(message)
        response.status_code = 201

        return response

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity =current_user)
        return {
            'access_token': access_token
        }