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


app = Flask(__name__, static_url_path='/static')
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


SAVE_DIR = "./static/images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)


#@app.route('/<path:filepath>')
@app.route('/static/images/<path:filepath>')
def send_js(filepath):
    return send_from_directory(SAVE_DIR, filepath)

@app.route('/camera', methods=['GET', 'POST'])
def camera():
    cap = cv2.VideoCapture(0)
    if cap.isOpened() is False:
        print("io error")
    else:
        ret, frame = cap.read()
        image_path="./images/"
        if (ret):
            cv2.imwrite(image_path + 'image.png', frame)
        else:
            print("read error")

        cap.release()
    return "camera"


@app.route('/start-camera', methods=['GET', 'POST'])
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


@app.route("/")
def route():
    return render_template("index.html")


@app.route('/pred-emotion')
def pred_emotion():

    filenames = os.listdir("../images")
    IMAGE_SIZE = (48, 48)

    # 画像を読み込む
    sample = random.choice(filenames)
    # img = load_img("./images/"+sample, target_size=IMAGE_SIZE)
    img = load_img("./images/image.png", target_size=IMAGE_SIZE)
    img_org = img

    model = load_model('../2020-09-29.h5')

    # 画像をnumpy配列に変換
    img = np.asarray(img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = img_gray.reshape(-1, 48, 48, 1) / 255.0

    # 予測させる
    pred = model.predict(img_gray)

    # 結果を表示（それぞれの表情の予測）
    print("Bad: ", pred[:, 0])
    print("Happy: ", pred[:, 1])

    angry = pred[:, 0][0].astype(np.float64)
    disgust = pred[:, 1][0].astype(np.float64)

    print(type(angry))

    response = {
        "bad": bad,
        "happy": happy,
    }

    return render_template(
        "index.html",
        predict = response
    )

@app.route('/hello',methods=['GET', 'POST'])
def index():
    return 'Hello'


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=3032)  # ポートの変更