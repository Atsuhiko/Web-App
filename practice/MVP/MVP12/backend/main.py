from flask import Flask, render_template
# import os

# textcount.pyから、text_count_bpモジュールをインポート
from textcount import text_count_bp
from uploadimage import upload_image_bp

# 静的ファイル：CSSやJavaScriptファイル
# static_folderをdistにし、フロントエンド(vue)とつなげる
app = Flask(__name__, static_folder='../dist/static', template_folder='../dist')

# Blueprintをアプリケーションに登録する
# アプリ側でルーティングを指定する場合、第２引数にURLを指定
app.register_blueprint(text_count_bp)
app.register_blueprint(upload_image_bp)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

if __name__ == '__main__':
    app.run()