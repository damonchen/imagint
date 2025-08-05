from flask_restful import Resource, reqparse
from pypinyin import lazy_pinyin


from . import api


class PinyinResource(Resource):

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("hanzi", type=str, location="json")
        args = parser.parse_args()

        hanzi = args.hanzi

        return {
            "pinyin": "_".join(lazy_pinyin(hanzi)),
        }


api.add_resource(PinyinResource, "/pinyin")
