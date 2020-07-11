# 参考: https://www.python.ambitious-engineer.com/archives/1630
# 参考: https://note.com/kamakiriphysics/n/n2aec5611af2a
# 参考:  https://qiita.com/Gen6/items/2979b84797c702c858b1

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, g, flash
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from stock_data import get_stock_data # プレイべーとライブラリーをimport

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

        # 会社名と年度をフロントエンドから取得
        company = request.form.get('company')
        year = request.form.get('year')

        # mycode_dic = {"KAO":4452, "KOSE":4922, "SHISEIDO":4911}
        if company == "kao":
            code = 4452
        elif company == "shiseido":
            code = 4911
        else:
            return render_template("index.html")

        # プロットデータの初期化 https://qiita.com/ganariya/items/dce51a15f82056e509dc
        # これを行わないとグラフデータがキャッシュされグラフが重ね書きされる。
        plt.clf()
        
        # 年度と会社コードから株価データをスクレイピング
        stock_df = get_stock_data(year, code)

        # グラフ作成
        line_plot = sns.lineplot(x=stock_df['date'], y=stock_df['close'] )
        filepath = "./graph/stock_graph_" + company + year + ".png"
        # グラフを画像として保存 https://qiita.com/ganariya/items/2ca66aa979e064af59a2
        figure = line_plot.get_figure()
        figure.savefig(filepath)

        return render_template("index.html", company=company, year=year, filepath=filepath)

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=3333) # ポートの変更