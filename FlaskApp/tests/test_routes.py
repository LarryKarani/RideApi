import unittest
import json

from FlaskApp.api.app import create_app

from FlaskApp.api.rideoffers import RideOffer
from FlaskApp.api.utils import Validator
from .dummy import  dummy_ride_offer_request,  dummy_ride_offer, dummy_incomplete_offer

app = create_app('testing')

validator = Validator()

class RegisterTestCase(unittest.TestCase):
    def setUp(self):
       self.ride_offer_instance = RideOffer()
       self.dummy_client = app.test_client()
       self.ride_offer = dummy_ride_offer
       self.request_j = dummy_ride_offer_request
       self.incomplete_offer = dummy_incomplete_offer
 
 #runs after every test
    def tearDown(self):
        RideOffer.ride_offers.clear()

    def test_get_all_ride_offers(self):
        self.response = self.dummy_client.get('/api/v1/rides')
        self.assertEqual(len(json.loads(self.response.data)), len(RideOffer.ride_offers))
        self.assertEqual(self.response.status_code, 200)


    def test_get_ride_with_correct_id(self):
        #add dummy user for testing
        self.ride_offer_instance.create_ride('larry','Kirinyaga','Tomboya','suxi','$20', '5','10:30')
        self.response = self.dummy_client.get('/api/v1/rides/<rideId:1>')
        
        self.assertTrue(self.response.status_code == 200)

    def test_get_ride_with_wrong_id(self):
        self.response = self.dummy_client.get('/api/v1/rides/<rideId:20>')
        self.assertTrue(json.loads(self.response.data), {'message':'ride offer for id provided doesnt exist'})
        self.assertTrue(self.response.status_code == 400)
    
    def test_create_ride_with_correct_details(self):
        self.response = self.dummy_client.post('/api/v1/rides', data= json.dumps(self.ride_offer), content_type='application/json')
        self.assertEqual(self.response.status_code, 201)

    def test_create_ride_with_incomplete_details(self):
        self.response = self.dummy_client.post('/api/v1/rides', data=json.dumps(self.incomplete_offer), content_type='application/json')
        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(json.loads(self.response.data), validator.validate(dummy_incomplete_offer, 'create_ride'))

    def  test_make_request_to_join_valid_details(self):

         self.response = self.dummy_client.post('/api/v1/rides/<rideId:1>/requests', data=json.dumps(self.request_j), content_type='application/json')
         
         self.assertEqual(json.loads(self.response.data), validator.validate(self.request_j, 'request_ride'))


    