import os
import sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash
import models
 
app = Flask(__name__)
app.config.from_object(__name__)
 
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db.sqlite3'),
    SECRET_KEY='foo-baa',
))
 
 
def connect_db():
    """ データベス接続に接続します """
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con
 
 
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
 
 
# 以下、画面に関わるメソッド
 
@app.route('/')
def index():
    """ 一覧画面 """
    con = get_db()
    results = models.select_all(con)
    return render_template('index.html', results=results)
 
 
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
 
    con = get_db()
 
    pk = models.insert(con, title, data, img)
    flash('登録処理が完了しました。')
    return redirect(url_for('view', pk=pk))
 
 
@app.route('/delete/<pk>', methods=['POST'])
def delete(pk):
    """ 結果削除処理 """
    con = get_db()
    models.delete(con, pk)
    flash('削除処理が完了しました。')
    return redirect(url_for('index'))
 
 
@app.route('/view/<pk>')
def view(pk):
    """ 結果参照処理 """
    con = get_db()
    result = models.select(con, pk)
    return render_template('view.html', result=result)
 
 
if __name__ == '__main__':
    app.run(app.run(debug=True, host='0.0.0.0', port=8000)) # ポートの変更