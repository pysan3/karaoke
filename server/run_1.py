from flask import Flask, request, g, redirect, url_for, render_template, flash
import sqlite3

import userDatabase2

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    USER_DATABASE='./user_db.sqlite3',
    USER_SONGS='./user_songs.sqlite3'
))

@app.route('/')
def index():

    return render_template('index2.html')