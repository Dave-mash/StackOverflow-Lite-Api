import unittest
from app import create_app

class BaseTest(unittest.TestCase):

    def setUp(self):
        """ Initializes app"""
        self.app = create_app('testing')
        self.app.testing = True
        self.client = self.app.test_client()
    
        self.user = {
            "first_name": "David",
            "last_name": "Mwangi",
            "username": "Dave",
            "email": "dave@gmail.com",
            "password": "abc123",
            "confirm_password": "abc123"
        }
        
        self.question = {
            "username": "John Doe",
            "email": "email@test.com",
            "title": "JWT",
            "question": "What is JWT in programming?"
        }

    def tearDown(self):
        self.app.testing = False
        self.app = None

if __name__ == '__main__':
    unittest.main(verbosity=2) # get the help string of every test and the result
