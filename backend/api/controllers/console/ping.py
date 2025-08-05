from flask_restful import Resource

from controllers.console import api


class PingApi(Resource):

    def get(self):
        return {"result": "pong"}


api.add_resource(Resource, "/ping")
