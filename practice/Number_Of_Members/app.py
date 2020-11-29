# 参考: https://www.python.ambitious-engineer.com/archives/1630
# 参考: https://note.com/kamakiriphysics/n/n2aec5611af2a
# 参考:  https://qiita.com/Gen6/items/2979b84797c702c858b1

import os
from datetime import datetime
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
        if csv:
            df = pd.read_csv(csv)
        else: # エラー処理
            return render_template("index.html", err_message_1="ファイルを選択してください！")

        # sns で描画
        # sns.set_style('whitegrid') # グラフの背景設定（白、グリッドあり）
        line_plot = sns.lineplot(x=df['日付'], y=df['メンバー合計数'])
        # line_plot = sns.lineplot(x="日付", y="メンバー合計数", data=df)
        fig = line_plot.get_figure()
        # グラフ画像を保存
        filepath = "./graph/" + datetime.now().strftime("%Y%m%d%H%M%S_") + "graph.png"
        fig.savefig(filepath)
        plt.close()

        return render_template("index.html", csv=csv, filepath=filepath)


if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=5554) # ポートの変更
