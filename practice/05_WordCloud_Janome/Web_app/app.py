# 参考: https://www.python.ambitious-engineer.com/archives/1630
# 参考: https://note.com/kamakiriphysics/n/n2aec5611af2a
# 参考:  https://qiita.com/Gen6/items/2979b84797c702c858b1

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g, flash
# import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from functions import create_wordcloud, get_text_from_URL

app = Flask(__name__)

SAVE_DIR = "result"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

@app.route('/result/<path:filepath>')
def send_js(filepath):
    return send_from_directory(SAVE_DIR, filepath)

@app.route("/", methods=["GET","POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":

        # フロントエンドから変数を取得
        url = request.form.get('url')
        mask = request.form.get('mask')

        if mask == "none":
            mask = None
        elif mask == "heart":
            mask = np.array(Image.open('./mask/heart.jpg'))
        elif mask == "cat":
            mask = np.array(Image.open('./mask/cat.png'))
        else:
            return render_template("index.html")
        
        # BS4でURLからテキストデータのみ取得
        text = get_text_from_URL(url)

        # WordCould を作製して画像ファイルを保存し、画像ファイルのパスを取得
        filepath = create_wordcloud(mask, text)

        return render_template("index.html", url=url, filepath=filepath)

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=5555) # ポートの変更