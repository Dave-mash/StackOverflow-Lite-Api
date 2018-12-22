import re
from werkzeug.security import generate_password_hash

class UserModel:
    """ add user a user to a database """

    def __init__(self):
        self.db = []

    def create_account(self, payload):
        generate_password_hash(payload['password'])
        payload["id"] = len(self.db)
        dup_email = [users for users in self.db if users['email'] == payload['email']]
        dup_username = [users for users in self.db if users['username'] == payload['username']]
        if dup_email:
            raise AssertionError('This account already exists')
        elif dup_username:
            raise AssertionError('This username is already taken')
        else:
            self.db.append(payload)
        return self.db

    def del_account(self, id):
        user = [user for user in self.db if user['id'] == id]
        self.db.remove(user[0])
        return self.db

    def edit_account(self, id, updates=None):
        user = [user for user in self.db if user['id'] == id]
        if updates:
            user = updates
            self.db[id] = user
            return self.db
        else:
            return user
