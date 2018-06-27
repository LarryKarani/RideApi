import unittest
import json

from FlaskApp.api.app import create_app

from FlaskApp.api.rideoffers import RideOffer
from FlaskApp.api.utils import Validator
from .dummy import ( dummy_ride_offer_request,  dummy_ride_offer, dummy_incomplete_offer,
                    dummy_user, dummy_login, dummy_incomplete_ride_offer_request )

app = create_app('testing')


class RegisterTestCase(unittest.TestCase):
    def setUp(self):
       self.dummy_client = app.test_client()
       self.ride_offer = dummy_ride_offer
       self.request_j = dummy_ride_offer_request
       self.incomplete_offer = dummy_incomplete_offer
       self.test_user = dummy_user
       self.test_login = dummy_login
       self.incomplete_request =dummy_incomplete_ride_offer_request
 
 #runs after every test
    def tearDown(self):
        RideOffer.ride_offers.clear()

    def test_get_all_ride_offers_with_correct_token(self):
        self.dummy_client.post('/api/v1/regester', data=json.dumps(self.test_user), content_type = 'application/json')
        self.response = self.dummy_client.post('api/v1/login', data=json.dumps(self.test_login), content_type="application/json")
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.get('/api/v1/rides', headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.assertEqual(self.response.status_code, 200)

    def test_get_all_ride_with_no_token(self):
        """Request all rides without sending in the required token"""
        self.dummy_client.post('/api/v1/regester', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('api/v1/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.get('api/v1/rides',headers={'content-type':'application/json'})
        self.auth_response = json.loads(self.response.data)
        self.assertNotIn(self.auth_response, RideOffer.ride_offers)
        self.assertTrue(self.response.status_code==401)

    def test_get_ride_with_correct_token(self):
        self.dummy_client.post('/api/v1/regester', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('api/v1/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data=json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.response = self.dummy_client.get('/api/v1/rides/<rideId:1>', headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        
        self.assertTrue(self.response.status_code == 200)

    def test_get_ride_with_invalid_token(self):
        self.dummy_client.post('/api/v1/regester', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('api/v1/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data=json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.response = self.dummy_client.get('/api/v1/rides/<rideId:1>', headers={'content-type':'application/json'})
        
        self.assertTrue(self.response.status_code == 401)



    def test_get_ride_with_wrong_id_and_correct_token(self):
        self.dummy_client.post('/api/v1/regester', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('api/v1/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.get('/api/v1/rides/<rideId:1>', headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.assertTrue(json.loads(self.response.data), {'message':'ride offer for id provided doesnt exist'})
        self.assertTrue(self.response.status_code == 400)
    
    def test_create_ride_with_correct_details_and_token(self):
        self.dummy_client.post('/api/v1/regester', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('api/v1/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data= json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.assertEqual(self.response.status_code, 201)

    def test_create_ride_with_correct_detail_no_token(self):
        self.dummy_client.post('/api/v1/regester', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('api/v1/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data= json.dumps(self.ride_offer), headers={'content-type':'application/json'})
        self.assertEqual(self.response.status_code, 401)


    def test_create_ride_with_incomplete_details(self):
        self.dummy_client.post('/api/v1/regester', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('api/v1/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data=json.dumps(self.incomplete_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.assertEqual(self.response.status_code, 400)


    def test_make_request_to_join_valid_details(self):
        self.dummy_client.post('/api/v1/regester', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('api/v1/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data= json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.response = self.dummy_client.post('/api/v1/rides/<rideId:1>/requests', data=json.dumps(self.request_j), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.assertEqual(self.response.status_code, 201)

    def test_request_to_join_no_token(self):
        self.dummy_client.post('/api/v1/regester', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('api/v1/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data= json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)}) 
        self.response = self.dummy_client.post('/api/v1/rides/<rideId:1>/requests', data=json.dumps(self.request_j), headers={'content-type':'application/json'})
        self.assertEqual(self.response.status_code, 401)

    def test_request_to_join_with_incomplete_details_with_tokens(self):
        self.dummy_client.post('/api/v1/regester', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('api/v1/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data= json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)}) 
        self.response = self.dummy_client.post('/api/v1/rides/<rideId:1>/requests', data=json.dumps(self.incomplete_request), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.assertEqual(self.response.status_code, 400)


