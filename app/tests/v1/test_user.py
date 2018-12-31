import json
from app.tests.v1.base_test import BaseTest

class TestUser(BaseTest):
    
    def post_req(self, path='/api/v1/auth/signup', data={}):
        """ This function makes use of test client to send POST requests """
        info_data = data if data else self.user
        res = self.client.post(path,
            data=json.dumps(info_data),
            content_type='application/json')
        return res

    def get_req(self, path='/api/v1/users'):
        """ This function makes use of the test client to send GET requests """
        res = self.client.get(path)
        return res

    def test_sign_up_user(self):
        """ Test that an unregistered user can sign up """
        # user instance
        payload = self.post_req(data=self.user)

        self.assertEqual(payload.status_code, 201)
        # self.assertEqual(self.user['username'], payload.json['username'])
        self.assertEqual(payload.json['message'], "{} registered successfully".format(self.user['email']))

    def test_sign_up_user_invalid_input(self):
        """ Test that registering with an invalid input will throw an error """

        # Invalid email
        user = { **self.user }
        user['email'] = 'davegmail.com'
        payload = self.post_req(data=user)
        self.assertEqual(payload.status_code, 400)
        self.assertEqual(payload.json['Error'], "Invalid email address")
        
        # Short username
        user2 = { **self.user }
        user2['username'] = 'D'
        payload = self.post_req(data=user2)
        self.assertEqual(payload.status_code, 400)
        self.assertEqual(payload.json['Error'], "Your name should be at least 3 to 20 characters")

        # Weak password
        user3 = { **self.user }
        user3['password'] = 'ab'
        user3['confirm_password'] = 'ab'
        payload = self.post_req(data=user3)
        self.assertEqual(payload.status_code, 400)
        self.assertEqual(payload.json['Error'], "Your password must have at least a lower,  uppercase, digit and special character and must be longer than 6 characters")

        # Unmatching passwords
        user4 = { **self.user }
        user4['password'] = 'abc123'
        user4['confirm_password'] = 'abc'
        payload = self.post_req(data=user4)
        self.assertEqual(payload.status_code, 400)
        self.assertEqual(payload.json['Error'], "Your passwords don\'t match")
        
        # Missed field
        user5 = { **self.user }
        user5['username'] = ''
        payload = self.post_req(data=user5)
        self.assertEqual(payload.status_code, 400)
        user4['confirm_password'] = 'abc'
        self.assertEqual(payload.json['Error'], "You missed a required field")

    def test_sign_up_user_existing_account(self):
        """ Test that registering with an existing username or email, will throw an error """

        user = { **self.user }
        payload = self.post_req(data=user)

        self.assertEqual(payload.status_code, 400)
        self.assertEqual(payload.json['Error'], "This account exists")
        
        user2 = { **self.user }
        user2['email'] = "mash@gmail.com"
        payload = self.post_req(data=user2)

        self.assertEqual(payload.json['Error'], "This username is taken")

    def test_log_in_unregistered_user(self):
        """ Test that an unregistered user can't log in """
        payload = {
            "email": self.user['email'],
            "password": self.user['password']
        }

        login = self.post_req('/api/v1/auth/login', payload)

        self.assertEqual(login.status_code, 404)
        self.assertEqual(login.json['Error'], "Account not found, try signing up")

    # def test_log_in_registered_user(self):
    #     """ Test that a registered user can log in """
    #     payload = {
    #         "email": self.user['email'],
    #         "password": self.user['password']
    #     }

        # signup = self.post_req(data=self.user)
    #     login = self.post_req('/api/v1/auth/login', payload)

        # self.assertEqual(signup.status_code, 201)
    #     self.assertEqual(login.json['Error'], "Account not found, try signing up")

    def test_get_all_users(self):
        """ Test that all users can be fetched """

        get = self.get_req()
        self.assertEqual(get.status_code, 200)
        self.assertEqual(get.json['users'], [])