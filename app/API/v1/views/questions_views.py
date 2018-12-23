from flask import request, jsonify, make_response
from app.API.v1.models.questions_model import QuestionsModel
from .. import version1

questions_list = QuestionsModel()

# @version1.route("/")
# def get_questions():
#     return make_response(jsonify({
#         "status": "ok",
#         "questions": questions_list.db
#     }), 201)


# @version1.route("/")
# def get():
#     return make_response(jsonify({
#         "users": registered_user.db
#     }), 201)
# @version1.route("/questions", methods=['POST'])
# def post_questions():
#     data = request.get_json()
#     # que = QuestionsModel(data['email'], data['question'])
#     # questions_list.append(que)
#     return make_response(jsonify({
#         "status": "ok",
#         # "questions": questions_list
#     }), 201)
