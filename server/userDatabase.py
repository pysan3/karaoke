import sqlite3
from matplotlib import pyplot as plt
from pandas.plotting import scatter_matrix
import pandas as pd
import time
import io
from flask import Flask, request, g, redirect, url_for, render_template, flash
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    USER_DATABASE='./user_db.sqlite3',
    SECRET_KEY='foo-baa',
))

def return_id(database, user_name):
    cur = database.cursor()
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

    def select_all(self):
        cur = self.database.cursor()
        cur = cur.execute('select id, user_name, user_password from user_datas order by id desc')
        return cur.fetchall()

    def logged_in(self, user_name, password):
        cur = self.database.cursor()
        cur = cur.execute('select * from user_datas where user_name=?', (user_name,))
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
        con = self.database.cursor()
        cur = con.execute('select * from user_datas where user_name=?', (user_name,))
        row = con.fetchone()
        if row == None:
            print('data doesnt exist')
            i = 0
            while True:
                con = self.database.cursor()
                cur = con.execute('select * from user_datas where id=?', (i,))
                if con.fetchone() == None:
                    con.execute('insert into user_datas (id, user_name, user_password) values (?, ?, ?)', [i, user_name, password])
                    self.database.commit()
                    break
                i += 1
            cur = con.execute('select * from user_datas where user_name=?', (user_name,))
            row = cur.fetchone()
            print('row =', row)
            print('row_id =', row['id'])
            return row['id']
        else:
            return "False"

class User:

    def __init__(self, id):
        pass