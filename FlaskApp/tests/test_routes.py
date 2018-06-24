import unittest
import json

from FlaskApp.app import create_app

from FlaskApp.api.rideoffers import RideOffer
from FlaskApp.api.utils import Validator
from .dummy import  dummy_ride_offer_request,  dummy_ride_offer, dummy_incomplete_offer

app = create_app('testing')

class RegisterTestCase(unittest.TestCase):
    def setUp(self):
       self.dummy_client = app.test_client()
       self.ride_offer = dummy_ride_offer
       self.request = dummy_ride_offer_request
       self.incomplete_offer = dummy_incomplete_offer
 
 #runs after every test
    def tearDown(self):
        RideOffer.ride_offers.clear()

    def test_get_all_ride_offers(self):
        self.response = self.dummy_client.get('/api/v1/rides')
        self.assertEqual(len(json.loads(self.response.data)), len(RideOffer.ride_offers))
        self.assertEqual(self.response.status_code, 200)


    def test_get_ride_with_correct_id(self):
        self.response = self.dummy_client.get('/api/v1/<rideId>')
        self.assertEqual(json.loads(self.response.data), RideOffer.get_ride_offer(json.loads(self.response.data)['id']))
        self.assertTrue(self.response.status_code == 200)

    def test_get_ride_with_wrong_id(self):
        self.response = self.dummy_client.get('/api/v1/<rideId>')
        self.assertTrue(json.loads(self.response.data), {'doesnt':'exist'})
        self.assertTrue(self.response.status_code == 404)
    
    def test_create_ride_with_correct_details(self):
        self.response = self.dummy_client.post('/api/v1/rides', data= json.dumps(self.ride_offer), content_type='application/json')
        self.assertEqual(self.response.status_code, 201)

    def test_create_ride_with_incomplete_details(self):
        self.response = self.dummy_client.post('/api/v1/rides', data=json.dumps(self.incomplete_offer), content_type='application/json')
        self.assertEqual(self.response.status_code, 401)
        self.assertEqual(json.loads(self.response.data), Validator.validate(dummy_incomplete_offer))

    def  test_make_request_to_join_valid_details(self):
         self.response = self.dummy_client.post('/api/v1/rides/<rideId>/requests', data=json.dumps(self.request), content_type='application/json')
         self.assertEqual(self.response.status_code, 201)
         self.assertEqual(json.loads(self.response.data), Validator.validate(self.request))


    