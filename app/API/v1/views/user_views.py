from flask import request, jsonify, make_response
from app.API.v1.utils.validators import RegistrationForm, LoginForm
from app.API.v1.models.user_model import UserModel
from app.API.v1.models.questions_model import QuestionsModel 
from .. import version1

user_model = UserModel()
questions_model = QuestionsModel()

@version1.route("/users")
def get():
    return make_response(jsonify({
        "users": user_model.db
    }), 200)

""" This route allows unregistered users to sign up """
@version1.route("/auth/signup", methods=['GET', 'POST'])
def registration():
    data = request.get_json()
    # questions = [que for que in questions_model.db if que['id'] == ]

    # Create user
    user1 = RegistrationForm(
        data['first_name'],
        data['last_name'],
        data['username'],
        data['email'],
        data['password'],
        data['confirm_password']
    )
    def json(error):
        return make_response(jsonify({
            "status": 400,
            "Error": error
        }), 400)

    # if user_model.dup_email:
    #     return json('This account already exists')
    # elif user_model.dup_username:
    #     return json('This username is taken')
    
    # prompt user fields
    if not user1.data_exists():
        return json('You missed a required field')
    elif not user1.valid_name():
        return json('Your name should be at least 3 to 20 characters')
    elif not user1.valid_email(data['email']):
        return json('Invalid email address')
    elif not user1.valid_confirm_password():
        return json('Your passwords don\'t match')
    elif not user1.valid_password(data['password']):
        return json('Your password must have at least a lower,  uppercase, digit and special character and must be longer than 6 characters')
    
    # Register user
    user_model.create_account(
        {
            "username": data['username'],
            "email": data['email'],
            "password": data['password'],
            # "questions": questions 
        }
    )
    if user_model.dup_email:
        return json(user_model.dup_email['Error'])
    elif user_model.dup_username:
        return json(user_model.dup_username['Error'])

    return make_response(jsonify({
        "status": "ok",
        "message": "{} registered successfully".format(data['email']),
        "username": data['username']
    }), 201)

""" This route allows registered users to log in """
@version1.route("/auth/login", methods=['GET', 'POST'])
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    # check for existing account
    if user_model.get_user(email, password) == 'SUCCESS':
        return make_response(jsonify({
            "message": "logged in as {}".format(email)
        }), 201)
    elif user_model.get_user(email, password) == 'FAILURE':
        return make_response(jsonify({
            "Error": "Account does not exist, try signing up"
        }), 404)
    elif user_model.get_user(email, password) == 'INVALID':
        return make_response(jsonify({
            "Error": "Invalid credentials, please check your email and password!"
        }), 404)

""" This route allows a registered user to log out """
@version1.route("/auth/logout", methods=['GET', 'POST'])
def logout():
    data = request.get_json()

    logged_user = [user for user in user_model.db if user['email'] == data['email']]
    
    if logged_user:
        return make_response(jsonify({
            "status": "ok",
            "message": "user {} logged out".format(data['email'])
        }), 201)
    elif not logged_user:
        return make_response(jsonify({
            "status": 404,
            "Error": "No logged users!"
        }), 404)


""" This route allows registered users to delete their existing accounts """
@version1.route("/account/delete/<int:delID>", methods=['GET', 'DELETE'])
def del_account(delID):
    data = request.get_json()
    
    """ compares and matches the details of the account """
    deleted = [deleted for deleted in user_model.db if deleted['email'] == data['email']]
    if deleted:
        user_model.del_account(delID)
        return make_response(jsonify({
            "status": "ok",
            "message": "account: '{}' was deleted".format(data['email'])
        }), 201)
    elif not deleted:
        return make_response(jsonify({
            "status": 404,
            "Error": "You are not logged in!"
        }), 404)

""" This route allows registered users to edit their accounts """
@version1.route("/account/edit/<int:editID>", methods=['GET', 'PUT'])
def edit_account(editID):
    data = request.get_json()

    """ compares and matches the details of the account """
    update = [update for update in user_model.db if update['email'] == data['email']]
    
    if update:
        user_model.edit_account(editID, data)
        return make_response(jsonify({
            "message": "{} account was updated".format(data['email']),
            "status": "ok"
        }), 201)
    else:
        return make_response(jsonify({
            "status": 404,
            "Error": "Sorry account does not exist!"
        }), 404)

