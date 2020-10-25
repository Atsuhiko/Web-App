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
from datetime import datetime # 井伊追加 filepathのタイムスタンプ取得のため
from PIL import Image # 画像の読み書きをするライブラリー pillow # 井伊追加


# app = Flask(__name__, static_url_path='/static')
app = Flask(__name__)
app.config.from_object(__name__)


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


# 画像を表示させるために必要なコード
@app.route('/images/<path:filepath>')
def send_js(filepath):
    return send_from_directory(SAVE_DIR, filepath)


# カメラ起動
@app.route('/start-camera')
def startCamera():
    cap = cv2.VideoCapture(0)

    if cap.isOpened() is False:
        print("IO Error")
    else:
        ret, frame = cap.read()
        image_path = "./images/"
        if (ret):
            cv2.imwrite(image_path + "image.png", frame)
        else:
            print("Read Error")

    cap.release()

    return render_template("index.html")


# トップページ
@app.route("/")
def route():
    return render_template("index.html")


# 表情判別
@app.route("/pred-emotion")
def pred_emotion():

    IMAGE_SIZE = (48, 48)

    # 画像を読み込む
    save_path = os.path.join(SAVE_DIR, "image.png")
    img = load_img(save_path, target_size=IMAGE_SIZE)
    img_org = img

    # モデルを読み込む
    model = load_model('../model_epoch100.h5')

    # 画像をnumpy配列に変換
    img = np.asarray(img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = img_gray.reshape(-1, 48, 48, 1) / 255.0

    # 予測させる
    pred = model.predict(img_gray)

    # 結果を表示（それぞれの表情の予測）
    print("Bad: ", pred[:, 0])
    print("Happy: ", pred[:, 1])

    bad = pred[:, 0][0].astype(np.float64)
    happy = pred[:, 1][0].astype(np.float64)

    response = {
        "bad": bad,
        "happy": happy,
    }

    # 今回判別させた画像を保存
    img = Image.open(save_path)
    filepath = "image" + datetime.now().strftime("_%Y%m%d%H%M%S") + ".png"
    save_path = os.path.join(SAVE_DIR, filepath)
    img.save(save_path)

    # フロントエンドに判別の結果を返す
    return render_template(
        "index.html",
        predict = response,
        filepath = filepath
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3032)  # ポートの変更