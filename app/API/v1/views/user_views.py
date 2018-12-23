from flask import request, jsonify, make_response
from app.API.v1.utils.validators import RegistrationForm, LoginForm
from app.API.v1.models.user_model import UserModel
from .. import version1

registered_user = UserModel()

# @version1.route("/")
# def get():
#     return make_response(jsonify({
#         "users": registered_user.db
#     }), 201)

""" This route allows unregistered users to sign up """
@version1.route("/auth/signup", methods=['GET', 'POST'])
def registration():
    data = request.get_json()
    
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

    # if registered_user.dup_email:
    #     return json('This account already exists')
    # elif registered_user.dup_username:
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
    registered_user.create_account(
        {
            "username": data['username'],
            "email": data['email'],
            "password": data['password']
        }
    )
    if registered_user.dup_email:
        return json(registered_user.dup_email['error'])
    elif registered_user.dup_username:
        return json(registered_user.dup_username['error'])

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
    exists = [ex for ex in registered_user.db if ex['email'] == data['email']]
    if exists:
        user1 = LoginForm(email, password)
        user1.valid_email(data['email'])
        user1.valid_password(data['password'])
        user1.logged = True

        logged_user = {
            "email": data['email'],
            "logged on": user1.logged,
            "questions": user1.questions
        }

        return make_response(jsonify({
            "status": "ok",
            "message": "logged in as {}".format(data['email']),
            "user": logged_user
        }), 201)
    else:
        return make_response(jsonify({
            "Error": "Account not found, try signing up"
        }), 401)


# """ This route allows a registered user to log out """
# @version1.route("/auth/logout/<int:logoutID>", methods=['GET', 'POST'])
# def logout(logoutID):
#     data = request.get_json()

    # if not data['user']['logged on']:
    #     return make_response(jsonify({
    #         "status": "400",
    #         "Error": "You are not logged in!"
    #     }), 201)
    # elif data['user']['logged on']:
    #     data['user']['logged'] = False
    #     return make_response(jsonify({
    #         "status": "ok",
    #         "message": "user {} logged out".format(data['email']),
    #         "user": data
    #     }), 201)

# """ This route allows registered users to delete their existing accounts """
@version1.route("/account/delete/<int:delID>", methods=['GET', 'DELETE'])
def del_account(delID):
    
    # matches out the id passed in it
    deleted = [remove for remove in registered_user.db if delID == remove['id']]
    registered_user.del_account(delID)

    return make_response(jsonify({
        "status": "ok",
        "message": "account: '{}' was deleted".format(deleted[0].get('email')),
        "users": registered_user.db
    }), 201)

""" This route allows registered users to edit their accounts """
@version1.route("/account/edit/<int:editID>", methods=['GET', 'PUT'])
def edit_account():
    # updates
    data = request.get_json()
    registered_user.edit_account(data['id'], data)

    return make_response(jsonify({
        "message": "{} account was updated".format(data['email']),
        "status": "ok",
        "user": registered_user.db
    }), 201)
