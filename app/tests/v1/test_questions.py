import json
from app.tests.v1.base_test import BaseTest
from app.API.v1.models.questions_model import QuestionsModel

questions_list = QuestionsModel()

class TestQuestions(BaseTest):
    
    def post_req(self, path='/api/v1/questions', data={}):
        """ This function makes use of test client to send POST requests """
        info_data = data if data else self.question
        res = self.client.post(path,
            data=json.dumps(info_data),
            content_type='application/json')
        return res

    def get_req(self, path='/api/v1/questions'):
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

        # Test for an error if no question is found
        payload = self.get_req('/api/v1/questions/0/')
        self.assertEqual(payload.status_code, 404)
        # self.assertEqual(payload.json['status'], 404)
        # self.assertEqual(payload.json['Error'], 'Page Not Found!')

        # Test for fetched question if found       
        questions_list.write_question({ **self.question })
        # self.post_req(data=self.question)
        # self.assertEqual(payload.status_code, 200)

    def test_post_a_question(self):
        """ Test that a question can be saved """

        que_item = {
            "question": self.question['question'],
            "answers": []
        }

        questions_list.write_question({ **self.question })
        payload = self.post_req(data=self.question)

        self.assertEqual(payload.status_code, 201)
        self.assertEqual(payload.json['username'], self.question['username'])
        self.assertEqual(payload.json['title'], self.question['title'])
        self.assertEqual(payload.json['question_item'], que_item)

    def test_edit_a_question(self):
        """ Test that a question can be updated """

        payload = self.post_req(path='/api/v1/questions/0/', data=self.question)
        # self.assertEqual(payload.status_code, 404)
        # self.assertEqual(payload.json['status'], 404)
        # self.assertEqual(payload.json['Error'], 'Page Not Found!')

    def test_delete_a_question(self):
        pass