# 参考: https://www.python.ambitious-engineer.com/archives/1630
# 参考: https://note.com/kamakiriphysics/n/n2aec5611af2a
# 参考: https://qiita.com/Gen6/items/2979b84797c702c858b1
# 参考: https://note.com/kamakiriphysics/n/n2aec5611af2a

import os
from io import BytesIO
from datetime import datetime
from flask import Flask, render_template, request, make_response
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

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

        kind = request.form.get('kind')
        if kind:
            from sklearn import datasets
            iris = datasets.load_iris()

            # 散布図
            fig1 = plt.figure(figsize=(8, 6))
            ax = fig1.add_subplot(111)
            markers = ['o', '^', 's']
            colors = ['blue', 'red', 'green']

            for i, label in enumerate(iris.target_names):
                ax.scatter(x=iris.data[iris.target==i, 0],
                    y=iris.data[iris.target==i, 1],
                    label=iris.target_names[i],
                    marker=markers[i],
                    c=colors[i])

            ax.legend(loc='best', fontsize=14)
            ax.set_title('Iris SepalLength / SepalWidth', size=16)
            ax.set_xlabel(iris.feature_names[0], size=14)
            ax.set_ylabel(iris.feature_names[1], size=14)

            canvas1 = FigureCanvasAgg(fig1)
            png_output1 = BytesIO()
            canvas1.print_png(png_output1)
            data1 = png_output1.getvalue()
            response1 = make_response(data1)
            response1.headers['Content-Type'] = 'image/png'

            # ３次元プロット
            y = iris.target

            fig2 = plt.figure(figsize=(12, 12))
            ax = fig2.add_subplot(111, projection='3d') # ※1 三次元プロットを指定

            markers = ['o', '^', 's']
            colors = ['blue', 'red', 'green']

            for i, label in enumerate(iris.target_names):
                ax.scatter(xs=iris.data[iris.target==i, 0], # x軸データ
                            ys=iris.data[iris.target==i, 1], # y軸データ
                            zs=iris.data[iris.target==i, 2], # z軸データ
                            label=iris.target_names[i],
                            marker=markers[i],
                            s=100,
                            c=colors[i])

            ax.legend(loc='best', fontsize=14)

            ax.set_title('Iris', size=16)
            ax.set_xlabel(iris.feature_names[0], size=14)
            ax.set_ylabel(iris.feature_names[1], size=14)
            ax.set_zlabel(iris.feature_names[2], size=14)

            canvas2 = FigureCanvasAgg(fig2)
            png_output2 = BytesIO()
            canvas2.print_png(png_output2)
            data2 = png_output2.getvalue()
            response2 = make_response(data2)
            response2.headers['Content-Type'] = 'image/png'

            if kind == "2d":
                # return render_template("index.html", response1=response1)
                return response1
            elif kind == "3d" :
                # return render_template("index.html", response2=response2)
                return response2
                
        else: # エラー処理
            return render_template("index.html", err_message="グラフの種類を選択してください！")

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=5555) # ポートの変更
