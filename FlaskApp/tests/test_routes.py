import py
import unittest
import json

from FlaskApp.api.app import create_app
from FlaskApp.api.db  import drop_all, con

from FlaskApp.api.utils import Validator
from .dummy import ( dummy_ride_offer_request,  dummy_ride_offer, dummy_incomplete_offer,
                    dummy_user, dummy_login, wrong_email, dummy_incomplete_ride_offer_request,
                    dummy_user_no_username, user_special_chars , new_user, dummy_wrong_login, dummy_login_test, test_user)

app = create_app('testing')


class RidesTestCase(unittest.TestCase):
    def setUp(self):
       self.dummy_client = app.test_client()
       self.ride_offer = dummy_ride_offer
       self.join_request = dummy_ride_offer_request
       self.incomplete_offer = dummy_incomplete_offer
       self.test_user = dummy_user
       self.test_login = dummy_login
       self.incomplete_request =dummy_incomplete_ride_offer_request
 
    def tearDown(self):
        drop_all(con)
          
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
        
        self.assertTrue(self.response.status_code==401)

    def test_get_ride_with_correct_token(self):
        """get ride with correct token"""
        self.dummy_client.post('/api/v1/auth/signup', data=json.dumps(self.test_user), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), headers={"content-type":"application/json"})
        self.token  = json.loads(self.response.data)['acces_token']
        self.response = self.dummy_client.post('/api/v1/rides', data=json.dumps(self.ride_offer), headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        self.response = self.dummy_client.get('/api/v1/rides/1', headers={'content-type':'application/json', 'Authorization':'Bearer {}'.format(self.token)})
        
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
        self.assertEqual(self.response.status_code, 400)

class RequestTestCase(unittest.TestCase):
    def setUp(self):
       self.dummy_client = app.test_client()
       self.ride_offer = dummy_ride_offer
       self.join_request = dummy_ride_offer_request
       self.incomplete_offer = dummy_incomplete_offer
       self.test_user = dummy_user
       self.test_login = dummy_login
       self.incomplete_request =dummy_incomplete_ride_offer_request

    def tearDown(self): 
        drop_all(con)

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

class RegesterTestcase(unittest.TestCase):
    
    def setUp(self):
        self.dummy_client = app.test_client()
        self.test_user = new_user
        self.empty_name =dummy_user_no_username
        self.special_chars_user = user_special_chars
        self.wrong_email= wrong_email
    def tearDown(self): 
        drop_all(con)


    def test_register_user_empty_username(self):
        self.response = self.dummy_client.post('/api/v1/auth/signup', data=json.dumps(self.empty_name), headers={'content-type':'application/json'})
        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(json.loads(self.response.get_data()), {'message':'please provide username'})

    def test_register_user_with_special_characters(self):
        self.response = self.dummy_client.post('/api/v1/auth/signup', data=json.dumps(self.special_chars_user), headers={'content-type':'application/json'})
        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(json.loads(self.response.get_data()), {'message':'invalid username'})

    def test_register_user_with_wrong_email_format(self):
         self.response = self.dummy_client.post('/api/v1/auth/signup', data=json.dumps(self.wrong_email), headers={'content-type':'application/json'})
         self.assertEqual(json.loads(self.response.get_data()), {'message':'Email is invalid'})
    
    def test_register_user_empty_user_with_incomplete_details(self):
        self.response = self.dummy_client.post('/api/v1/auth/signup', data=json.dumps(self.empty_name), headers={'content-type':'application/json'})
        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(json.loads(self.response.get_data()), {'message':'please provide username'})

    def test_register_user_twice(self):
        self.response = self.dummy_client.post('/api/v1/auth/signup', data=json.dumps(self.empty_name), headers={'content-type':'application/json'})
        self.response = self.dummy_client.post('/api/v1/auth/signup', data=json.dumps(self.empty_name), headers={'content-type':'application/json'})
        self.assertEqual(self.response.status_code, 400)
        self.assertEqual(json.loads(self.response.get_data()), {'message':'please provide username'})
        

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.dummy_client = app.test_client()
        self.test_user = test_user
        self.login_user = dummy_login
        self.wrong_login = dummy_wrong_login
        self.test_login = dummy_login_test

    def test_login_registered_user(self):
        self.dummy_client.post('/api/v1/auth/signup', data=json.dumps(self.test_user), content_type = 'application/json')
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.test_login), content_type="application/json")
        self.assertEqual(self.response.status_code , 200)

    def test_login_for_unregisterd_user(self):
        self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.wrong_login), content_type="application/json")
        self.assertEqual(json.loads(self.response.get_data()) , { "message": "User {} does't exist".format(self.wrong_login["username"])})

    def test_login_with_wrong_password(self):
         self.response = self.dummy_client.post('/api/v1/auth/login', data=json.dumps(self.wrong_login), content_type="application/json")
         self.assertEqual(json.loads(self.response.get_data()) , { "message": "User {} does't exist".format(self.wrong_login["username"])})

