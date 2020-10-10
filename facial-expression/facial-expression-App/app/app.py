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


SAVE_DIR = "/Users/yuriko-kakino/Documents/Web-App/facial-expression/facial-expression-App/app/static/images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)


#@app.route('/<path:filepath>')
@app.route('/static/images/<path:filepath>')
def send_js(filepath):
    return send_from_directory(SAVE_DIR, filepath)


@app.route('/start-camera')
def startCamera():
    cap = cv2.VideoCapture(0)

    if cap.isOpened() is False:
        print("IO Error")
    else:
        ret, frame = cap.read()
        image_path = "/Users/yuriko-kakino/Documents/Web-App/facial-expression/facial-expression-App/app/static/images/"
        if (ret):
            cv2.imwrite(image_path + "image.png", frame)
        else:
            print("Read Error")

    cap.release()
    response = {
        "message": "ok"
    }
    return jsonify(response)
    


@app.route("/")
def route():
    return render_template("index.html")


@app.route("/pred-emotion")
def pred_emotion():

    filenames = os.listdir("../images")
    IMAGE_SIZE = (48, 48)

    # 画像を読み込む
    sample = random.choice(filenames)
    # img = load_img("./images/"+sample, target_size=IMAGE_SIZE)
    img = load_img("/Users/yuriko-kakino/Documents/Web-App/facial-expression/facial-expression-App/app/static/images/image.png", target_size=IMAGE_SIZE)
    img_org = img

    # model = load_model('../2020-09-27-epoch50.h5')
    model = load_model('../2020-09-29.h5')

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
    """
    return render_template(
        "index.html",
        angry=angry,
        disgust=disgust,
        fear=fear,
        happy=happy,
        sad=sad,
        surprise=surprise,
        neutral=neutral
    )
    """
    
    response = {
        "angry": angry,
        "disgust": disgust,
        "fear": fear,
        "happy": happy,
        "sad": sad,
        "surprise": surprise,
        "neutral": neutral,
    }
    
    """
    response = [angry,
            disgust,
            fear,
            happy,
            sad,
            surprise,
            neutral]
    """

    # return response
    # response = make_response(response_body)
    return render_template(
        "index.html",
        predict = response
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3032)  # ポートの変更