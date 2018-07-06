import unittest
import json

from FlaskApp.api.app import create_app, con
from FlaskApp.api.db  import drop_all


from .dummy import *

app=create_app('testing')


class RequestTestCase(unittest.TestCase):
    def setUp(self):
       self.dummy_client = app.test_client()
       self.ride_offer = dummy_ride_offer
       self.join_request = dummy_ride_offer_request
       self.incomplete_offer = dummy_incomplete_offer
       self.test_user = dummy_user
       self.test_login = dummy_login
       self.incomplete_request =dummy_incomplete_ride_offer_request


    def test_request_to_join_no_token(self):
        self.dummy_client.post('/api/v1/auth/signup', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data= json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)}) 
        self.response = self.dummy_client.post('/api/v1/rides/1/requests', data=json.dumps(self.join_request), headers={'content-type':'application/json'})
        self.assertEqual(self.response.status_code, 401)
        self.assertEqual(json.loads(self.response.get_data()), {'msg':'Missing Authorization Header'})

    def test_request_to_join_with_incomplete_details_with_tokens(self):
        self.dummy_client.post('/api/v1/auth/signup', data= json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data= json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)}) 
        self.response = self.dummy_client.post('/api/v1/rides/1/requests', data=json.dumps(self.incomplete_request), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(json.loads(self.response.get_data()), {'message':'please provide destination'})
