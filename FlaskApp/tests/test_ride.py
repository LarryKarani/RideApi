import unittest
import json

from FlaskApp.api.app import create_app, con
from FlaskApp.api.db  import drop_all


from .dummy import *

app=create_app('testing')
        
class RidesTestCase(unittest.TestCase):
    def setUp(self):
       self.dummy_client = app.test_client()
       self.ride_offer = dummy_ride_offer
       self.join_request = dummy_ride_offer_request
       self.incomplete_offer = dummy_incomplete_offer
       self.test_user = dummy_user
       self.test_login = dummy_login
       self.incomplete_request =dummy_incomplete_ride_offer_request
 
    
          
    def test_get_all_ride_offers_with_correct_token(self):
        self.dummy_client.post('/api/v1/auth/signup', data=json.dumps(self.test_user), content_type = 'application/json')
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), content_type="application/json")
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.get('/api/v1/rides', headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        
        self.assertEqual(self.response.status_code, 200)

    def test_get_all_ride_with_no_token(self):
        """Request all rides without sending in the required token"""
        self.dummy_client.post('/api/v1/auth/signup', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.get('api/v1/rides',headers={'content-type':'application/json'})
        self.auth_response = json.loads(self.response.data)
        self.assertEqual(self.auth_response, {"msg":"Missing Authorization Header"})
        self.assertTrue(self.response.status_code==401)

    def test_get_ride_with_correct_token(self):
        """get ride with correct token"""
        self.dummy_client.post('/api/v1/auth/signup', data=json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data=json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.response = self.dummy_client.get('/api/v1/rides/1', headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.assertEqual= (json.loads(self.response.data), {"gggh":'hhj'})
        self.assertTrue(self.response.status_code == 200)

    def test_get_ride_with_invalid_token(self):
        self.dummy_client.post('/api/v1/auth/signup', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data=json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.response = self.dummy_client.get('/api/v1/rides/1', headers={'content-type':'application/json'})
        
        self.assertTrue(self.response.status_code == 401)

    def test_get_ride_with_wrong_id_and_correct_token(self):
        self.dummy_client.post('/api/v1/auth/signup', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.get('/api/v1/rides/1000', headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.assertEqual(json.loads(self.response.data), {'message':'ride offer for id provided doesnt exist'})
        self.assertTrue(self.response.status_code == 400)
    
    def test_create_ride_with_correct_details_and_token(self):
        self.dummy_client.post('/api/v1/auth/signup', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data= json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.assertEqual(self.response.status_code, 201)

    def test_create_ride_with_correct_detail_no_token(self):
        self.dummy_client.post('/api/v1/auth/signup', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data= json.dumps(self.ride_offer), headers={'content-type':'application/json'})
        self.assertEqual(self.response.status_code, 401)

    def test_create_ride_with_incomplete_details(self):
        self.dummy_client.post('/api/v1/auth/signup', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data=json.dumps(self.incomplete_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.assertEqual(json.loads(self.response.data), {"message":"please provide depature_time"})
        self.assertEqual(self.response.status_code, 400)
