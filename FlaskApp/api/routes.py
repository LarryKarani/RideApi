from flask_jwt_extended import(create_access_token, create_refresh_token,
                               jwt_required, jwt_refresh_token_required, get_jwt_identity)
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, redirect


from .utils import Validator
from .db import return_user
from .db_config import con

cursor = con.cursor()
parser = reqparse.RequestParser()
parser.add_argument('username', help='username cannot be blank', required=True)
parser.add_argument('password', help='password cannot be blank', required=True)


class Home(Resource):
    def get(self):
        return redirect("https://ridemyway6.docs.apiary.io/", code=302)


class Login(Resource):
    def post(self):

        data = parser.parse_args()
        get_user_query = 'SELECT username, password FROM users WHERE "username"=\'{}\''.format(
            data['username'])

        current_user = return_user(con, get_user_query)

        if not current_user:
            return {'message': 'User {} does\'t exist'.format(data['username'])}

        if check_password_hash(current_user[0][1], data['password'].strip()):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            response = jsonify({
                "message": "logged in as {}".format(current_user[0][0]),
                "acces_token": access_token,
                'refresh_token': refresh_token
            })

            response.status_code = 200

            return response

        else:
            return {'message': 'Wrong credentials'}


class Register(Resource):
    def post(self):
        """"register a new user"""

        data = request.get_json(force=True)
        """pass through the validator method to confirm details"""
        message = Validator(data, 'reg').validate()

        if message:
            response = jsonify(message)
            response.status_code = 400

            return response

        """check if email is already registered"""

        check_query = 'SELECT * FROM users WHERE "email" =\'{}\'and "username"=\'{}\''.format(
            data['email'], data['username'])

        user_exist = return_user(con, check_query)

        if user_exist:
            response = jsonify({'message': 'username already registered'})
            response.status_code = 400
            return response

        new_user_query = 'INSERT INTO users (username, email, password)\
         VALUES(\'%s\',\'%s\',\'%s\');' % (data['username'].strip(), data['email'].strip().lower(),
                                           generate_password_hash(data['password'].strip()))

        cursor.execute(new_user_query)

        message = {

            "message": "User created successfully"
        }

        response = jsonify(message)
        response.status_code = 201

        return response


class AllRides(Resource):

    @jwt_required
    def get(self):
        get_rides_query = 'SELECT array_to_json(array_agg(rides)) FROM rides '
        all_rides = return_user(con, get_rides_query)
    
        return all_rides

    @jwt_required
    def post(self):
        """creates a new ride offer"""
        content = request.get_json(force=True)
        message = Validator(content, 'create_ride').validate()

        if message:
            response = jsonify(message)
            response.status_code = 400

            return response

        user = get_jwt_identity()

        get_user_query = 'SELECT Id from users WHERE username=\'{}\''.format(
            user)

        current_user = return_user(con, get_user_query)

        user_id = current_user[0][0]

        new_ride_query = 'INSERT INTO rides (current_location, destination, depature_time, seats_available, cost,user_id)\
         VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' % (content['current_location'].strip(), content['destination'].strip().lower(),
                                                                content['depature_time'].strip(), content['seats_available'].strip(), content['cost'], user_id)

        cursor.execute(new_ride_query)

        message = {

            'message': "ride offer created succesfully"
        }

        response = jsonify(message)
        response.status_code = 201

        return response


class GetRide(Resource):

    @jwt_required
    def get(self, rideId):
        # retrieves a single ride offer from the list of all rides

        get_ride_query = 'SELECT array_to_json(array_agg(rides)) FROM rides WHERE "id"=\'{}\''.format(
            rideId)
        ride = return_user(con, get_ride_query)
       
        if ride[0][0] is None:
            
            response = jsonify(
                {"message": "ride offer for id provided doesnt exist"})
            response.status_code = 400
            return response
       
        response = jsonify(ride)
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

        get_ride_query = 'SELECT current_location, depature_time FROM rides WHERE "id"=\'{}\''.format(
            rideId)
        ride = return_user(con, get_ride_query)

        if not ride:
            response = jsonify({'message': 'ride offer does not exist'})
            response.status_code = 400

        new_request_query = 'INSERT INTO request (Username,current_location, destination, depature_time, request_id)\
         VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' % (data['Username'].strip(), data['current_location'].strip().lower(),
                                                         data['destination'].strip(), data['depature_time'].strip(), rideId)

        cursor.execute(new_request_query)

        message = {
            'request': 'created succesfully',

        }
        response = jsonify(message)
        response.status_code = 201

        return response

    @jwt_required
    def get(self, rideId):
        get_request_query = 'SELECT current_location, destination FROM request WHERE "request_id"=\'{}\''.format(
            rideId)

        all_rides = return_user(con, get_request_query)

        if not all_rides:
            message = {
                "msg": f"no request for rideId {rideId}"
            }

            response = jsonify(message)
            response.status_code = 400

            return response

        message = {
            "request": all_rides
        }
        response = jsonify(message)
        response.status_code = 200

        return response


class RideOfferResponse(Resource):
    @jwt_required
    def put(self, rideId, requestId):

        data = request.get_json(force=True)
        message = Validator(data, 'reply').validate()

        get_ride_query = 'SELECT current_location, depature_time FROM rides WHERE "id"=\'{}\''.format(
            rideId)
        get_request_query = f'SELECT * FROM request WHERE "id"= \'{requestId}\''
        ride = return_user(con, get_ride_query)
        req = return_user(con, get_request_query)

        if message:
            return message

        if not ride:
            message = {
                "message": f"ride with ride Id {rideId} does not exist"
            }

            response = jsonify(message)
            response.status_code = 400

            return response
        if not req:
            message = {
                "message": f"ride with request Id {requestId} does not exist"
            }

            response = jsonify(message)
            response.status_code = 400

            return response

        new_reply_query = 'INSERT INTO response (reply)VALUES(\'%s\');' % (
            data['reply'].strip())
        cursor.execute(new_reply_query)

        message = {
            "msg": f"request {data['reply']}"

        }
        response = jsonify(message)
        response.status_code = 201

        return response


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {
            'access_token': access_token
        }
