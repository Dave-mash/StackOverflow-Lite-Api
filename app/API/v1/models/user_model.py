from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    """ add user a user to a database """

    def __init__(self):
        self.dup_email = None,
        self.dup_username = None,
        self.db = []

    def create_account(self, payload):
        payload["id"] = len(self.db)
        payload['password'] = generate_password_hash(payload['password'])
        
        # Check for duplicate email and username
        self.dup_email = [users for users in self.db if users['email'] == payload['email']]
        self.dup_username = [users for users in self.db if users['username'] == payload['username']]
        
        if self.dup_email:
            self.dup_email = {"Error": "This account exists"}
        else:
            self.dup_email = None
        
        if self.dup_username:
            self.dup_username = {"Error": "This username is taken"}
        else:
            self.dup_username = None
        
        if not self.dup_email and not self.dup_username:
            self.db.append(payload)
            return self.db

    def get_user(self, email, password):
        user = [user for user in self.db if email == user['email']]

        if user:
            if check_password_hash(user[0]['password'], password):
                return 'SUCCESS'
            else:
                return 'INVALID'
        else:
            return 'FAILURE'

    def edit_account(self, id, updates=None):
        from app.API.v1.views.user_views import user_model as registered_user
        for i in range(len(registered_user.db)):
            if registered_user.db[i]["id"] == id:
                registered_user.db[i] = updates
                return registered_user.db

    def del_account(self, id):
        user = [user for user in self.db if user['id'] == id]
        self.db.remove(user[0])
        return self.db
