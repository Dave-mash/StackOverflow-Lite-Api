from flask import request, jsonify, make_response
from app.API.v1.utils.validators import RegistrationForm, LoginForm
from app.API.v1.models.user_model import UserModel
from app.API.v1.models.questions_model import QuestionsModel 
from .. import version1

user_model = UserModel()
questions_model = QuestionsModel()

@version1.route("/")
def get():
    return make_response(jsonify({
        "users": user_model.db
    }), 201)

""" This route allows unregistered users to sign up """
@version1.route("/auth/signup", methods=['GET', 'POST'])
def registration():
    data = request.get_json()
    # questions = [que for que in questions_model.db if que['id'] == ]

    # Create user
    user1 = RegistrationForm(
        data['username'],
        data['email'],
        data['password'],
        data['confirm_password']
    )
    def json(error):
        return make_response(jsonify({
            "status": 400,
            "error": error
        }), 201)

    # if user_model.dup_email:
    #     return json('This account already exists')
    # elif user_model.dup_username:
    #     return json('This username is taken')
    
    # prompt user fields
    if not user1.data_exists():
        return json('You missed a required field')
    elif not user1.valid_username():
        return json('Username should be at least 3 to 20 characters')
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
            "logged on": user_model.logged[0]
            # "questions": questions 
        }
    )
    if user_model.dup_email:
        return json(user_model.dup_email['error'])
    elif user_model.dup_username:
        return json(user_model.dup_username['error'])

    return make_response(jsonify({
        "status": "ok",
        "message": "registration successful",
        "username": data['username']
    }), 201)

""" This route allows registered users to log in """
@version1.route("/auth/login", methods=['GET', 'POST'])
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    # check for existing account
    exists = [ex for ex in user_model.db if ex['email'] == data['email']]
    question = [que for que in questions_model.db if que['email'] == data['email']]
    if exists:
        log_user = LoginForm(email, password)
        log_user.get_questions(question[0])
        log_user.valid_email(data['email'])
        log_user.valid_password(data['password'])
        exists[0]["logged on"] = True

        return make_response(jsonify({
            "logged": exists[0]["logged on"],
            "message": "logged in as {}".format(data['email'])
        }), 201)
    else:
        return make_response(jsonify({
            "Error": "Account not found, try signing up"
        }), 401)


""" This route allows a registered user to log out """
@version1.route("/auth/logout", methods=['GET', 'POST'])
def logout():
    data = request.get_json()

    logged_user = [user for user in user_model.db if user['email'] == data['email']]
    
    if logged_user:
        logged_user[0]['logged on'] = False
        return make_response(jsonify({
            "status": "ok",
            "message": "user {} logged out".format(data['email'])
        }), 201)
    elif not logged_user:
        return make_response(jsonify({
            "status": 404,
            "Error": "You are not logged in!"
        }), 404)


""" This route allows registered users to delete their existing accounts """
@version1.route("/account/delete/<int:delID>", methods=['GET', 'DELETE'])
def del_account(delID):
    data = request.get_json()
    
    """ compares and matches the details of the account """
    deleted = [
        deleted for deleted in user_model.db if deleted['email'] == data['email'] and deleted['password'] == data['password']
    ]
    if deleted:
        if user_model.db[delID]['logged on']:
            user_model.del_account(delID)
            return make_response(jsonify({
                "status": "ok",
                "message": "account: '{}' was deleted".format(data['email'])
            }), 201)
        else:
            return make_response(jsonify({
                "Error": "You're not logged in!"
            }), 404)
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
    update = [
        update for update in user_model.db if update['email'] == data['email'] and update['password'] == data['password']
    ]
    if update:
        if user_model.db[editID]['logged on']:
            user_model.edit_account(editID, data, user_model.logged)
            return make_response(jsonify({
                "message": "{} account was updated".format(data['email']),
                "status": "ok"
            }), 201)
        else:
            return make_response(jsonify({
                "Error": "You're not logged in!"
            }), 404)

    else:
        return make_response(jsonify({
            "status": 404,
            "Error": "Sorry account does not exist!"
        }), 404)

