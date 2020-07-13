# 参考: https://www.python.ambitious-engineer.com/archives/1630
# 参考: https://note.com/kamakiriphysics/n/n2aec5611af2a
# 参考:  https://qiita.com/Gen6/items/2979b84797c702c858b1

import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    g,
    flash,
)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno
import lib.utils as utils
import traceback

app = Flask(__name__)

SAVE_DIR = "graph"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)


@app.route("/graph/<path:filepath>")
def send_js(filepath):
    return send_from_directory(SAVE_DIR, filepath)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":

        # debug (https://bit.ly/3iCGQOa)
        for k, v in request.args.items():
            print(
                "app.upload_file: URL Query Parameter {",
                k,
                ":",
                v,
                "(",
                type(v),
                ")",
                "}",
            )
        for k, v in request.form.items():
            print(
                "app.upload_file: Request Parameter {", k, ":", v, "}",
            )
        for k, v in request.files.items():
            print("app.upload_file: Upload File {", k, ":", v, "}")

        # リクエストパラメータを取得
        csv = request.files["csv"]
        kind = request.form.get("kind")

        # リクエストパラメータをチェック
        if "" == csv.filename:
            return render_template("index.html", error_msg="ファイルを選択してください！")
        if "" == kind:
            return render_template("index.html", error_msg="グラフの種類を選択してください！")

        # CSVデータを読み込み
        df = pd.read_csv(csv)

        # レスポンス処理
        if kind == "pairplot":
            graph_name = "seaborn pairplot"
            img = utils.draw_pairplot(df)
            return render_template(
                "index.html", filepath=img, csv=csv, graph_name=graph_name
            )
        elif kind == "lmplot":
            graph_name = "seaborn lmplot"
            img = utils.draw_lmplot(df)
            return render_template(
                "index.html", filepath=img, csv=csv, graph_name=graph_name
            )
        elif kind == "duplicated":
            graph_name = "duplicated records"
            img = utils.draw_duplicated(df)
            return render_template(
                "index.html", filepath=img, csv=csv, graph_name=graph_name
            )
        elif kind == "missing":
            graph_name = "missing values"
            img = utils.draw_missing(df)
            return render_template(
                "index.html", filepath=img, csv=csv, graph_name=graph_name
            )
        elif kind == "univariate":
            graph_name = "univariate analysis"
            img = utils.draw_univariate_analysis(df)
            return render_template(
                "index.html", filepath=img, csv=csv, graph_name=graph_name
            )
        else:
            return render_template("index.html", error_msg="不正なグラフの種類が選択されました！")


@app.errorhandler(pd.errors.EmptyDataError)
@app.errorhandler(pd.errors.ParserError)
@app.errorhandler(pd.errors.UnsortedIndexError)
@app.errorhandler(UnicodeDecodeError)
def handle_pandas_excetion(e):
    print(traceback.format_exc())
    return (
        render_template("index.html", error_msg="対応していないフォーマットのCSVデータがアップロードされました！",),
        200,
    )


@app.errorhandler(Exception)
def handle_exception(e):
    print(traceback.format_exc())
    return (
        render_template("index.html", error_msg="意図しない例外が発生しました！",),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3333)  # ポートの変
