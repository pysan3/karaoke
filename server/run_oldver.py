from flask import Flask, request, g, redirect, url_for, render_template, flash
import sqlite3

import models

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE='./db.sqlite3',
    SECRET_KEY='foo-baa',
))

# 以下、DB接続関連の関数
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
    flash("hogehoge")
    return redirect(url_for('view', pk=pk))

@app.route('/delete/<pk>', methods=['POST'])
def delete(pk):
    """ 結果削除処理 """
    database = get_db()
    models.delete(database, pk)
    flash("fugafuga")
    return redirect(url_for('index'))

@app.route('/view/<pk>')
def view(pk):
    """ 結果参照処理 """
    database = get_db()
    result = models.select(database, pk)
    return render_template('view.html', result=result)

if __name__ == '__main__':
    app.run()