from flask import Flask, request, jsonify, make_response
from app.API.v1.utils.validators import RegistrationForm, LoginForm
from app.API.v1.models.user_model import UserModel
from .. import version1

registered_user = UserModel()

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

    # validate user
    user1.valid_username()
    user1.valid_email(data['email'])
    user1.valid_password(data['password'])
    user1.valid_confirm_password()

    # Register user
    registered_user.create_account(
        {
            "username": data['username'],
            "email": data['email'],
            "password": data['password'],
        }
    )

    return make_response(jsonify({
        "status": "ok",
        "username": data['username']
    }), 201)

@version1.route("/auth/login", methods=['GET', 'POST'])
def login():
    data = request.get_json()
    
    # log in info
    email = data['email'],
    password = data['password'],
    
    # check for existing account
    dups = [ex for ex in registered_user.db if ex['email'] == data['email']]
    if dups:
        user1 = LoginForm(email, password)
        user1.valid_email(data['email'])
        user1.valid_password(data['password'])
    else:
        raise AssertionError('You have to log in first')

    return make_response(jsonify({
        "status": "ok",
        "message": "logged in as {}".format(data['email'])
    }), 201)

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
