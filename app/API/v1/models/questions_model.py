
class QuestionsModel:
    """ add a question to the database """

    def __init__(self):
        self.db = []

    def write_question(self, item):
        if item:
            self.db.append(item)

    def edit_question(self, id, updates=None):
        que = [que for que in self.db if que['id'] == id]
        if que:
            que = updates
            self.db[id] = que
            return self.db
        else:
            return que
    def del_question(self, id):
        que = [que for que in self.db if que['id'] == id]
        self.db.remove(que[0])
        return self.db
