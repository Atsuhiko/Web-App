# 参考: https://qiita.com/redshoga/items/60db7285a573a5e87eb6
# 参考: https://teratail.com/questions/244325
# 参考: https://qiita.com/Susasan/items/52d1c838eb34133042a3

import cv2
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
# import pandas as pd
from datetime import datetime
import os
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
# 判別アルゴリズムのインポート
from image_process import Predict_Dogs_Cats


app = Flask(__name__)

SAVE_DIR = "images"

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
        model = load_model('vgg16_model.h5') # 学習ずみモデルの読み込み
        result = Predict_Dogs_Cats(input_img, model)
        print(result)

        cat = result[0][0]
        dog = result[0][1]

        if result[0][0] > result[0][1]:
            prediction = "cat"
        else:
            prediction = "dog"

        # 判別後のラベルと時刻を付けてファイル名を付け、画像を保存
        filepath = prediction + datetime.now().strftime("_%Y%m%d%H%M%S") + ".jpg"
        save_path = "./images/" + filepath
        # save_path = os.path.join(SAVE_DIR, filepath)
        cv2.imwrite(save_path, input_img)

        return  render_template("index.html", 
                                save_path=save_path, filepath=filepath, 
                                prediction=prediction, cat=cat, dog=dog)


if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=3030) # ポートの変更
