#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import random
from flask import Flask, make_response,render_template, request, redirect, url_for, send_from_directory, g, flash, jsonify
from keras.preprocessing.image import load_img
import numpy as np
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
from datetime import datetime
from PIL import Image

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String #DBのテーブルの型をインポート


app = Flask(__name__)
app.config.from_object(__name__)

"""
# DB接続用
app.config['SECRET_KEY']='secret key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///flask.sqlite' # DBへのパス

# SQLiteのDBテーブル情報
class Result(db.Model):
    # __tablename__='Result'
    id = db.Column(Integer, primary_key=True)
    bad = db.Column(float)
    happy = db.Column(float)

# DB作成
db.create_all()
"""



# jinzaの{}がvueとかぶるので、<>に変更
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


# 画像保存先フォルダの設定
SAVE_DIR = "images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)


# トップページ
@app.route("/")
def route():
    return render_template("index.html")


# 画像を表示させるために必要なコード
@app.route('/images/<path:filepath>')
def send_js(filepath):
    return send_from_directory(SAVE_DIR, filepath)


# カメラ起動
@app.route('/start-camera')
def startCamera():

    # VideoCaptureクラスのインスタンスを生成
    # 引数にカメラの番号。内蔵webカメラ使用時は0を指定
    cap = cv2.VideoCapture(0)

    if cap.isOpened() is False:  # 正常に読み込めなかった場合
        print("IO Error")
    else:
        # readメソッド
        # 返り値１　ret: フレームの画像が読み込めたか　/  返り値２  frame: 画像の配列（ndarray)
        ret, frame = cap.read()
        image_path = "./images/"

        if (ret):  # 正常に保存できた場合
            # imwriteメソッド　引数１：画像のパス（拡張子はjpgやpng等）　引数２：画像を表すndarrayオブジェクト
            cv2.imwrite(image_path + "image.png", frame)
        else:
            print("Read Error")

    cap.release() # カメラデバイスを終了する

    return render_template("index.html")


# 表情判別
@app.route("/pred-emotion")
def pred_emotion():

    # 画像サイズ
    IMAGE_SIZE = (48, 48)

    # 画像を読み込む
    save_path = os.path.join(SAVE_DIR, "image.png") # pathを連結する
    img = load_img(save_path, target_size=IMAGE_SIZE)   # 画像を読み込むと同時にリサイズ

    app.logger.debug(img) # ログ出力

    # モデルを読み込む
    model = load_model('../model_epoch100.h5')

    # 画像をnumpy配列に変換
    img = np.asarray(img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = img_gray.reshape(-1, 48, 48, 1) / 255.0
    # numpy配列の変形 -1：1列データ　48,48：縦横　1:要素１つ
    # 255で割って正規化。0-255 → 0-1の範囲になることで扱いやすくなる

    app.logger.debug(img) # ログ出力
    app.logger.debug(img_gray) # ログ出力

    # 予測させる
    pred = model.predict(img_gray)
    # [[0.7929875  0.20701244]]

    # 結果を表示（それぞれの表情の予測）
    print("Bad: ", pred[0][0])
    print("Happy: ", pred[0][1])

    bad = pred[0][0].astype(np.float64)
    happy = pred[0][1].astype(np.float64)

    app.logger.debug(pred) # ログ出力

    response = {
        "bad": bad,
        "happy": happy,
    }

    # 今回判別させた画像を保存
    img = Image.open(save_path) # PILで画像読み込み
    filepath = "image" + datetime.now().strftime("_%Y%m%d%H%M%S") + ".png" # ファイル名を指定
    save_path = os.path.join(SAVE_DIR, filepath)  # パスとファイル名を連結
    img.save(save_path) # 画像を保存


    # フロントエンドに判別の結果を返す
    return render_template(
        "index.html",
        predict = response,
        filepath = filepath
    )

@app.route('/save-emotion', mothods=['POST'])
def save_emotion():
    if request.method =='POST':
        bad = request.form['bad']
        happy = request.form['happy']
        data = Result(bad=bad, happy=happy)
        db.session.add(data)
        db.seddion.commit()
        db.session.close()
        Result_info = db.session.query(Result.id, Result.bad, Result.happy).all()
        return render_template('index.html', Result_info=Result_info)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3032)  # ポートの変更