'''from flask import Blueprint, jsonify, request, session
from flask_restful import Api, Resource
import json

# Blueprintオブジェクトを生成
# アプリケーションの機能を分解する
# (オブジェクト名, __name__, ルーティング)
# ルーティングはBlueprintオブジェクト生成時または、main.pyへの登録時のどちらかに行う
text_count_bp = Blueprint('text_count', __name__, url_prefix='/api/text-count')


# @text_count_bp.route('/api/text-count', methods=["POST"])
class TextCount(Resource):
    def text_count(self):
        # if request.method == "POST":
            input_data = request.json
            result_data = {
                'text': input_data['text'],
                'count': len(
                    input_data['text'])}
            return jsonify(result_data)


text_count = Api(text_count_bp)
text_count.add_resource(TextCount, '')
'''


from flask import Blueprint, jsonify, request, session
from flask_restful import Api, Resource
import json

# postされたテキストをカウントするapi(POSTメソッド)
text_count_bp = Blueprint('text_count', __name__, url_prefix='/api/textcount')
class TextCount(Resource):
    def post(self):

        # postされたデータを読み込み
        input_data = request.json

        # 入力文字列の文字数をカウント
        result_data = {'text':input_data['text'], 'count':len(input_data['text'])}

        return jsonify(result_data)

text_count = Api(text_count_bp)
text_count.add_resource(TextCount, '')