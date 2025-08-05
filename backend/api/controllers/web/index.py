import datetime

from flask import current_app
from flask_restful import Resource
from . import api


class IndexApi(Resource):
    def get(self):
        return {
            "welcome": "Web",
            "api_version": "v1",
            "server_version": current_app.config.get("CURRENT_VERSION"),
        }


api.add_resource(IndexApi, "/")
