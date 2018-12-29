import json
from app.tests.v1.base_test import BaseTest

class TestQuestions(BaseTest):
    
    def post_req(self, path='/api/v1/questions/', data={}):
        """ This function makes use of test client to send POST requests """
        info_data = data if data else self.question
        res = self.client.post(path,
            data=json.dumps(info_data),
            content_type='application/json')
        return res

    def get_req(self, path='/api/v1/questions/'):
        """ This function makes use of the test client to send GET requests """
        res = self.client.get(path)
        return res

    def test_get_all_questions(self):
        """ Test that all questions can be fetched """

        get = self.get_req()
        self.assertEqual(get.status_code, 200)
        self.assertEqual(get.json['questions'], [])

    def test_get_a_single_question(self):
        """ Test that a single question can be fetched """

        que = { **self.question }
        que['email'] = "email.com" 
        payload = self.post_req(data=que)
        self.assertEqual(payload.status_code, 400)
        self.assertEqual(payload.json['Error'], "Your name should be at least 3 to 20 characters")
