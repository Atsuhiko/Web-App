# -*- coding: utf-8 -*-
# 参考: https://qiita.com/redshoga/items/60db7285a573a5e87eb6
# 参考: https://teratail.com/questions/244325
# 参考: https://qiita.com/Susasan/items/52d1c838eb34133042a3
# DB参照：https://www.python.ambitious-engineer.com/archives/1640

import os
import cv2
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g, flash, jsonify
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

app = Flask(__name__, static_folder='../dist/static', template_folder='../dist')

# Customize Directive
# https://www.subarunari.com/entry/2017/09/30/003944
# jinja2のディレクティブをFlask経由で変更できます。
# 以下の例では、{{...}} {%...%} {#...#}をそれぞれ<<...>> <%...%> <#...#>に変更。
jinja_options = app.jinja_options.copy()
jinja_options.update({
    'block_start_string': '<%',
    'block_end_string': '%>',
    'variable_start_string': '<<',
    'variable_end_string': '>>',
    'comment_start_string': '<#',
    'comment_end_string': '#>'
})
app.jinja_options = jinja_options


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

@app.route('/axios-test')
def hello():
    helloResult = {
        "result": request.json['text'].split()
    }
    return jsonify(helloResult)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        # 画像として読み込み
        """stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        input_img = cv2.imdecode(img_array, 1)
        """
        # stream = request.form['image'].stream
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        input_img = cv2.imdecode(img_array, 1)

        # イヌと猫の判別
        model = load_model('model_cnn.h5')  # 学習ずみモデルの読み込み
        result = Predict_Dogs_Cats(input_img, model)
        print(result)

        cat = float(result[0][0])  # floar() しないとSQLにrealとして渡せない
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
        results = db.selerect_all(con)
        response = {
            'cat': cat,
            'dog': dog,
            'results': results,
        }
        return jsonify(response)

        """return render_template(
            "index.html",
            filepath=filepath,
            prediction=prediction,
            cat=cat,
            dog=dog,
            results=results,
            animal=[
                'dog',
                'cat',
                'pig'])  # フロントエンドの Vue.js で使用"""
        # https://ymgsapo.com/2019/10/12/pass-value-template/


# 終了したとき db 接続を close する
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3031)  # ポートの変更
