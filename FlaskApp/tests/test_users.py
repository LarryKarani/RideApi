import unittest
import json
from .dummy import *
from FlaskApp.api.app import create_app, con
from FlaskApp.api.db  import drop_all

app=create_app('testing')
class RegesterTestcase(unittest.TestCase):
    
    def setUp(self):
        self.dummy_client = app.test_client()
        self.test_user = new_user
        self.empty_name =dummy_user_no_username
        self.special_chars_user = user_special_chars
        self.wrong_email= wrong_email
   

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

