import sqlite3
from matplotlib import pyplot as plt
from pandas.plotting import scatter_matrix
import pandas as pd
import time
import io

user_list = [
    ["takuto", "000"]
]

def return_id(database, user_name):
    cur = database.execute('select * from user_datas where user_name=?', (user_name,))
    row = cur.fetchone()
    return row["id"]

class Database:

    def __init__(self, database):
        self.database = database

    def get(self, user_name, password):
        for i in range(len(user_list)):
            if user_list[i][0] == user_name:
                if user_list[i][1] == password:
                    return i
        return "False"

    def select_all(self):
        cur = self.database.execute('select * from user_datas')
        return cur.fetchall()

    def logged_in(self, user_name, password):
        """
        try:
            cur = self.database.execute('select * from user_datas where user_name=?', (user_name,))
            row = cur.fetchone()
            print("cur found")
            for i in range(4):
                print(row[i])
            if row["user_password"] == password:
                return row["id"]
            else:
                return "False"
        except:
            return "False"
        """
        cur = self.database.execute('select * from user_datas where user_name=?', (user_name,))
        row = cur.fetchone()
        if row == None:
            print('user_name doesnt exist')
        elif row['user_password'] == password:
            print('right password')
            return row['id']
        else:
            print('error happenned')
        return "False"

    def signed_in(self, user_name, password):
        cur = self.database.execute('select * from user_datas where user_name=?', (user_name,))
        row = cur.fetchone()
        if row == None:
            self.database.execute('insert into user_datas (user_name, user_password) values (?, ?)', (user_name, password))
            cur = self.database.execute('select * from user_datas where user_name=?', (user_name,))
            row = cur.fetchone()
            print('row =', row)
            return row['id']
        else:
            return "False"

class User:

    def __init__(self, id):
        self.user = user_list[id]