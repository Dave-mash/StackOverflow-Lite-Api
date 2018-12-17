from flask import Blueprint, request, render_template, jsonify
# from app.validators.validators import Validator
from .. import version1

data = [
    {
        "id": "123",
        "author": "Doe",
        "question": "what is Flask",
        "answers": []
    },
    {
        "id": "124",
        "author": "Jane",
        "question": "How to pull a git repo",
        "answers": []
    },
    {
        "id": "125",
        "author": "Doe",
        "question": "How to test python data",
        "answers": []
    }
]

""" fetch all the questions """
@version1.route('/questions')
def questions():
    return jsonify(data)

""" fetch a question """
@version1.route('/questions/<int:questionID>')
def question_item():
    for question in data:
        if question["id"] == '124':
            current = question
    return jsonify(current)

""" fetch an answer to a question """
@version1.route('/questions/<int:questionID>/answers')
def answer():
    for question in data:
        if question["id"] == '123':
            current = question["answers"]
    return jsonify(current)

""" post a question """
@version1.route('/post', methods=['POST'])
def post_questions():
    if request.method == 'POST':
        que = {
            "id": "126",
            "title": "stack overflow-lite",
            "description": "How does stack overflow-lite work",
            "answers": []
        }

        if not que["description"]:
            raise AssertionError('No description provided')
        else:
            data.append(que)

    return jsonify(data)


""" post an answer to a question """
@version1.route('/questions/<int:questionID>', methods=['PUT'])
def post_answer(questionID):
    if request.method == 'POST':
        que = {
            "id": "234",
            "author": "Jane",
            "answer": "Use git pull origin repo-name"
        }
        for question in data:
            if question["id"] == questionID:
                question["answers"].append(que)
                return data
            
    return jsonify(data)
    

""" delete a question """
@version1.route('/questions/<int:questionID>', methods=['DELETE'])
def del_question(questionID):
    que = [question for question in data if question["id"] == questionID]
    data.remove(que[0])
    return jsonify(data)
