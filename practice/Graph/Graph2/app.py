# 参考: https://www.python.ambitious-engineer.com/archives/1630
# 参考: https://note.com/kamakiriphysics/n/n2aec5611af2a
# 参考:  https://qiita.com/Gen6/items/2979b84797c702c858b1

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g, flash
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

SAVE_DIR = "graph"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

@app.route('/graph/<path:filepath>')
def send_js(filepath):
    return send_from_directory(SAVE_DIR, filepath)

@app.route("/", methods=["GET","POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":

        # csv ファイルを DataFrame に読み込み
        csv = request.files['csv']
        df = pd.read_csv(csv)

        # sns で描画
        sns_plot_1 = sns.pairplot(df, hue ="label")
        sns_plot_2 = sns.lmplot(x="a1", y="a4", data=df, hue="label")

        # グラフ画像を保存
        filepath_1 = "./graph/graph1.png"
        filepath_2 = "./graph/graph2.png"
        sns_plot_1.savefig(filepath_1)
        sns_plot_2.savefig(filepath_2)

        return  render_template("index.html", csv=csv, filepath_1=filepath_1, filepath_2=filepath_2)

if __name__ == '__main__':
    app.run(app.run(debug=True,  host='0.0.0.0', port=3030)) # ポートの変更
