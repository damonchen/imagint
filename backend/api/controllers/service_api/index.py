import datetime

from flask import current_app
from flask_restful import Resource
from . import api
from api.libs.decorator import unified_response
from api.libs.response import make_response


class IndexApi(Resource):
    def get(self):
        return make_response(
            {
                "welcome": "Web",
                "api_version": "v1",
                "server_version": current_app.config.get("CURRENT_VERSION"),
            }
        )


api.add_resource(IndexApi, "/")
