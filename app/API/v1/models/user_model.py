from werkzeug.security import generate_password_hash

class UserModel:
    """ add user a user to a database """

    def __init__(self, logged=False):
        self.logged = logged,
        self.dup_email = None,
        self.dup_username = None,
        self.db = []

    def create_account(self, payload):
        generate_password_hash(payload['password'])
        payload["id"] = len(self.db)
        
        # Check for duplicate email and username
        self.dup_email = [users for users in self.db if users['email'] == payload['email']]
        self.dup_username = [users for users in self.db if users['username'] == payload['username']]
        
        if self.dup_email:
            self.dup_email = {"error": "This account exists"}
        else:
            self.dup_email = None
        
        if self.dup_username:
            self.dup_username = {"error": "This username is taken"}
        else:
            self.dup_username = None
        
        if not self.dup_email and not self.dup_username:
            self.db.append(payload)
            return self.db

    def edit_account(self, id, updates=None, logged=False):
        from app.API.v1.views.user_views import registered_user
        if logged:    
            for i in range(len(registered_user.db)):
                if registered_user.db[i]["id"] == id:
                    registered_user.db[i] = updates
                    return registered_user.db

    def del_account(self, id):
        user = [user for user in self.db if user['id'] == id]
        self.db.remove(user[0])
        return self.db
