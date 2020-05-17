# 参考: https://qiita.com/redshoga/items/60db7285a573a5e87eb6
# 参考: https://teratail.com/questions/244325
# 参考: https://qiita.com/Susasan/items/52d1c838eb34133042a3
# DB参照：https://www.python.ambitious-engineer.com/archives/1640

import os
import cv2
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g, flash
import sqlite3
import numpy as np
# import pandas as pd
from datetime import datetime
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model

# 判別アルゴリズムのインポート
from image_process import Predict_Dogs_Cats
# DBライブラリーインストール
import db


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


SAVE_DIR = "images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)


@app.route('/images/<path:filepath>')
def send_js(filepath):
    return send_from_directory(SAVE_DIR, filepath)


@app.route("/", methods=["GET","POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":

        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        input_img = cv2.imdecode(img_array, 1)

        # イヌと猫の判別
        model = load_model('model_cnn.h5') # 学習ずみモデルの読み込み
        result = Predict_Dogs_Cats(input_img, model)
        print(result)

        cat = float(result[0][0]) # floar() しないとSQLにrealとして渡せない
        dog = float(result[0][1])

        if result[0][0] > result[0][1]:
            prediction = "cat"
        else:
            prediction = "dog"

        # 判別後のラベルと時刻を付けてファイル名を付け、画像を保存
        filepath = prediction + datetime.now().strftime("_%Y%m%d%H%M%S") + ".jpg"
        # save_path = "./images/" + filepath
        save_path = os.path.join(SAVE_DIR, filepath)
        cv2.imwrite(save_path, input_img)

        con = get_db()
        pk = db.insert(con, filepath, prediction, dog, cat)

        # """ 一覧画面 """
        results = db.select_all(con)

        return  render_template("index.html", 
                                filepath=filepath, prediction=prediction, cat=cat, dog=dog,
                                results=results)

 
# 終了したとき db 接続を close する
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == '__main__':
    app.run(app.run(debug=True,  host='0.0.0.0', port=1010)) # ポートの変更
