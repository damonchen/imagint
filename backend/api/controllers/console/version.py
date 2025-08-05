import logging

from flask import current_app
from flask_restful import Resource, marshal_with, reqparse
import requests

from . import api

class VersionApi(Resource):

    default_version = {
                'version': '0.0.1',
                'release_date': '',
                'release_notes': '',
                'has_auto_update': False,
            }

    # @marshal_with(fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('current_version', type=str, required=True, location='args')
        args = parser.parse_args()

        check_update_url = current_app.config["CHECK_UPDATE_URL"]

        if not check_update_url:
            return self.default_version

        try:
            response = requests.get(check_update_url, {'current_version': args.get('current_version')})
        except Exception as error: 
            logging.warning('check update version error %s', error)
            return self.default_version

        content = response.json()
        return {
                "version": content['version'],
                "release_date": content['releaseDate'],
                "release_notes": content['releaseNotes'],
                "has_auto_update": content['hasAutoUpdate'],
            }


api.add_resource(VersionApi, "/version")