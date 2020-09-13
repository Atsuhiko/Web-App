from flask import Blueprint, jsonify, request, session
from flask_restful import Api, Resource
import json

text_count_bp = Blueprint('text_count', __name__, url_prefix='/api/post')


class TextCount(Resource):
    def post(self):
        input_data = request.json
        result_data = {
            'text': input_data['text'],
            'count': len(
                input_data['text'])}
        return jsonify(result_data)


text_count = Api(text_count_bp)
text_count.add_resource(TextCount, '')
