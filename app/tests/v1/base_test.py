import unittest
from app import create_app

class BaseTest(unittest.TestCase):

    def setUp(self):
        """ Initializes app"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
        self.user = {
            "first_name": "David",
            "last_name": "Mwangi",
            "username": "Dave",
            "email": "dave@gmail.com",
            "password": "abc123",
            "confirm_password": "abc123"
        }
        
    def tearDown(self):
        
        with self.app.app_context():
            self.app.testing = False
            self.app = None

if __name__ == '__main__':
    unittest.main(verbosity=2) # get the help string of every test and the result
