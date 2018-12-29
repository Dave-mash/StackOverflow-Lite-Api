from datetime import datetime

class UserModel:
    """ add user a user to a database """

    def __init__(
        self,
        Fname='Fname',
        Lname='Lname',
        username='username',
        email='username@demo.com',
        password='password',
        logged=False
    ):
        self.logged = logged,
        self.Fname = Fname
        self.Lname = Lname
        self.username = username
        self.email = email
        self.password = password
        self.date_created = datetime.now()
        self.db = []

    def create_account(self, payload):
        payload["id"] = len(self.db)
        self.db.append(payload)
        return self.db

    def edit_account(self, id, updates=None, logged=False):
        from app.API.v1.views.user_views import user_model as registered_user
        if logged:    
            for i in range(len(registered_user.db)):
                if registered_user.db[i]["id"] == id:
                    registered_user.db[i] = updates
                    return registered_user.db

    def del_account(self, id):
        user = [user for user in self.db if user['id'] == id]
        self.db.remove(user[0])
        return self.db
