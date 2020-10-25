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

app = Flask(__name__) # 井伊書き換え
app.config.from_object(__name__)

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


SAVE_DIR = "images"  # 井伊書き換え
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)


#@app.route('/<path:filepath>')
@app.route('/images/<path:filepath>')
def send_js(filepath):
    return send_from_directory(SAVE_DIR, filepath)


@app.route('/start-camera')
def startCamera():
    cap = cv2.VideoCapture(0)

    if cap.isOpened() is False:
        print("IO Error")
    else:
        ret, frame = cap.read()
        # image_path = "images"
        image_path = os.path.join(SAVE_DIR, "image.png") # 井伊書き換え
        if (ret):
            # cv2.imwrite(image_path + "image.png", frame)
            cv2.imwrite(image_path, frame)
        else:
            print("Read Error")

    cap.release()
    return render_template("index.html")

@app.route("/")
def route():
    return render_template("index.html")


@app.route("/pred-emotion")
def pred_emotion():

    # filenames = os.listdir("../images")
    filenames = os.listdir("/images") # 井伊書き換え
    IMAGE_SIZE = (48, 48)

    # 画像を読み込む
    
    # img = load_img("/images/image.png", target_size=IMAGE_SIZE)
    save_path = os.path.join(SAVE_DIR, "image.png") # 井伊書き換え
    img = load_img(save_path, target_size=IMAGE_SIZE) # 井伊書き換え
    img_org = img

    # model = load_model('../2020-09-27-epoch50.h5')
    model = load_model('2020-09-29.h5')

    # 画像をnumpy配列に変換
    img = np.asarray(img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = img_gray.reshape(-1, 48, 48, 1) / 255.0

    # 予測させる
    pred = model.predict(img_gray)

    # 結果を表示（それぞれの表情の予測）
    print("Angry: ", pred[:, 0])
    print("Disgust: ", pred[:, 1])
    print("Fear: ", pred[:, 2])
    print("Happy :", pred[:, 3])
    print("Sad: ", pred[:, 4])
    print("Surprise: ", pred[:, 5])
    print("Neutral: ", pred[:, 6])

    angry = pred[:, 0][0].astype(np.float64)
    disgust = pred[:, 1][0].astype(np.float64)
    fear = pred[:, 2][0].astype(np.float64)
    happy = pred[:, 3][0].astype(np.float64)
    sad = pred[:, 4][0].astype(np.float64)
    surprise = pred[:, 5][0].astype(np.float64)
    neutral = pred[:, 6][0].astype(np.float64)

    print(type(angry))

    # plt.imshow(img_org) # 入力したオリジナルイメージ

    response = {
        "angry": angry,
        "disgust": disgust,
        "fear": fear,
        "happy": happy,
        "sad": sad,
        "surprise": surprise,
        "neutral": neutral,
    }

    # Webカメラから取得した画像データpillowを用いて再び読み込みタイムスタンプを付けて保存
    img = Image.open(save_path)
    filepath = "image" + datetime.now().strftime("_%Y%m%d%H%M%S") + ".png"
    save_path = os.path.join(SAVE_DIR, filepath)
    img.save(save_path)

    # return response
    # response = make_response(response_body)
    return render_template(
        "index.html",
        predict = response,
        filepath = filepath # これが重要
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3033)  # ポートの変更