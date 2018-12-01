from flask import Flask, request, g, redirect, url_for, render_template, flash
import sqlite3

import models
import userDatabase

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE='./db.sqlite3',
    USER_DATABASE='./user_db.sqlite3',
    SECRET_KEY='foo-baa',
))

# 以下、画面/機能毎の関数
@app.route('/')
def index():
    """ 一覧画面 """
    database = get_db()
    results = models.select_all(database)
    return render_template('index.html', results=results)

@app.route('/log_in')
def log_in():
    return render_template('log_in.html')

@app.route('/logged_in', methods=['POST'])
def logged_in():
    flash('hogehoge')
    user_name = request.form['user_name']
    password = request.form['password']
    database = userDatabase.get_db()
    db = userDatabase.Database(database)
    user_id = db.logged_in(user_name, password)
    print(user_id)
    if user_id != "False":
        return redirect(url_for('user_page'))
    else:
        return redirect(url_for('log_in'))

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/signed_in', methods=['POST'])
def signed_in():
    user_name = request.form['user_name']
    password = request.form['password']
    database = userDatabase.get_db()
    db = userDatabase.Database(database)
    user_id = db.signed_in(user_name, password)
    print(user_id)
    if user_id != 'False':
        return redirect(url_for('user_page'))
    else:
        return redirect(url_for('sign_in'))

@app.route('/user_page')
def user_page():
    database = userDatabase.get_db()
    db = userDatabase.Database(database)
    results = db.select_all()
    return redirect(url_for('index', results=results))

@app.route('/database')
def database():
    database = userDatabase.get_db()
    db = userDatabase.Database(database)
    results = db.select_all()
    return render_template('database.html', results=results)

@app.route('/records')
def records():
    return render_template('records.html')

@app.route('/audio_upload')
def audio_upload():
    return render_template('audio_upload.html')

@app.route('/voice_upload')
def voice_upload():
    return render_template('voice_upload.html')

@app.route('/points')
def points():
    return render_template('points.html')


# ignore below
def connect_db():
    """ データベース接続に接続します """
    database = sqlite3.connect(app.config['DATABASE'])
    database.row_factory = sqlite3.Row
    return database

def get_db():
    """ connectionを取得します """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """ db接続をcloseします """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/create')
def create():
    """ 新規作成画面 """
    return render_template('edit.html')

@app.route('/analysis', methods=['POST'])
def analysis():
    """ 分析実行処理 """

    title = request.form['title']
    data = request.form['data']
    img = models.create_scatter(data)

    database = get_db()

    pk = models.insert(database, title, data, img)
    flash('hogehoge')
    return redirect(url_for('view', pk=pk))

@app.route('/delete/<pk>', methods=['POST'])
def delete(pk):
    """ 結果削除処理 """
    database = get_db()
    models.delete(database, pk)
    flash('fugafuga')
    return redirect(url_for('index'))

@app.route('/view/<pk>')
def view(pk):
    """ 結果参照処理 """
    database = get_db()
    result = models.select(database, pk)
    return render_template('view.html', result=result)

if __name__ == '__main__':
    app.run()