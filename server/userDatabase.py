import sqlite3

user_list = [
    ["takuto", "000"]
]

class Database:

    def __init__(self):
        self.user_id = 0

    def get(self, user_name, password):
        for i in range(len(user_list)):
            if user_list[i][0] == user_name:
                if user_list[i][1] == password:
                    return i
        return "False"

class User:

    def __init__(self, id):
        self.user = user_list[id]