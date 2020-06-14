# 参考: https://qiita.com/redshoga/items/60db7285a573a5e87eb6
# 参考: https://teratail.com/questions/244325

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
#from image_process import canny
from image_process import build_vgg, Predict_Dogs_Cats
from datetime import datetime
import os
import string
import random

import gc
import tensorflow as tf
from tensorflow import keras

SAVE_DIR = "./images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

app = Flask(__name__, static_url_path="")

# def random_str(n):
#     return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

@app.route('/')
def index():
    return render_template('index.html', images=os.listdir(SAVE_DIR)[::-1])


@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(SAVE_DIR, path)


# 画像の読み込み: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b
# HTML から変数の受信：https://christmas-cookies.hatenablog.com/entry/2018/08/04/144127
@app.route('/upload', methods=['POST']) 
def upload():
    if request.files['image']:

        IMAGE_WIDTH=224
        IMAGE_HEIGHT=224
        IMAGE_SIZE=(IMAGE_WIDTH, IMAGE_HEIGHT)

        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)

        # 画像判別
        #img = canny(img)
        model = build_vgg()
        output = Predict_Dogs_Cats(img, model)
        print(output)
        # メモリの解放は上手く行かなかった。
        # del model
        # keras.backend.clear_session() # ←これです
        # gc.collect()

        # 保存
        #dt_now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        dt_now = datetime.now().strftime("_%M_%S")
        save_path = os.path.join(SAVE_DIR, output + dt_now + ".png")
        print(save_path)
        cv2.imwrite(save_path, img)
        print("save", save_path)

        return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True,  host='0.0.0.0', port=2020) # ポートの変更