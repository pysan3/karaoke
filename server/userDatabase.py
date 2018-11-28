import sqlite3
from matplotlib import pyplot as plt
from pandas.plotting import scatter_matrix
import pandas as pd
import time
import io
from flask import Flask, request, g, redirect, url_for, render_template, flash
app = Flask(__name__)
app.config.from_object(__name__)

user_list = [
    ["takuto", "000"]
]

app.config.update(dict(
    DATABASE='./db.sqlite3',
    USER_DATABASE='./user_db.sqlite3',
    SECRET_KEY='foo-baa',
))

def return_id(database, user_name):
    cur = database.execute('select * from user_datas where user_name=?', (user_name,))
    row = cur.fetchone()
    return row["id"]

def connect_db():
    """ データベース接続に接続します """
    database = sqlite3.connect(app.config['USER_DATABASE'])
    database.row_factory = sqlite3.Row
    return database

def get_db():
    """ connectionを取得します """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

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
        cur = self.database.execute('select id, user_name, user_password from user_datas order by id desc')
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
            print('row_id =', row['id'])
            return row['id']
        else:
            return "False"

class User:

    def __init__(self, id):
        self.user = user_list[id]