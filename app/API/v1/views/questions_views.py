from flask import request, jsonify, make_response
import re
from app.API.v1.models.questions_model import QuestionsModel
from app.API.v1.utils.validators import Questions
from .. import version1

questions_list = QuestionsModel()

""" This route grabs all questions and displays them """
@version1.route("/questions", methods=['GET'])
def get_questions():
    return make_response(jsonify({
        "status": "ok",
        "questions": questions_list.db
    }), 201)

""" This route grabs a single question and displays """
@version1.route("/questions/<int:questionID>", methods=['GET'])
def get_question(questionID):
    data = request.get_json()
    question = [que for que in questions_list.db if que['id'] == questionID]
    if question:
        return make_response(jsonify({
            "status": "ok",
            "question": question[0]
        }), 201)

""" This route posts a question """
@version1.route("/questions", methods=['POST'])
def post_question():
    data = request.get_json()

    question = Questions(data['email'], data['title'], data['question'])
    if not question.valid_email(data['email']):
        return make_response(jsonify({ "Error": "Ivalid email" }), 404)
    elif len(data['question']) < 20:
        return make_response(jsonify({ "Error": "A question should be at least 20 characters long!" }), 404)
    else:
        que_item = {
            "question": data['question'],
            "answers": []
        }
        questions_list.write_question({
            "username": data['username'],
            "email": data['email'],
            "title": data['title'],
            "question": que_item
        })
        return make_response(jsonify({
            "username": data['username'],
            "title": data['title'],
            "question_item": que_item
        }), 201)

