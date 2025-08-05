from flask import Response, request
from flask_restful import Resource
from werkzeug.exceptions import NotFound

from controllers.files import api
from libs.exceptions import BaseHTTPException
from services.attachment_service import AttachmentImageService
from services.errors.file import UnsupportedFileTypeError as _UnsupportedFileTypeError


class UnsupportedFileTypeError(BaseHTTPException):
    error_code = "unsupported_file_type"
    description = "File type not allowed."
    code = 415


class ImagePreviewApi(Resource):
    def get(self, attachment_id):
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        sign = request.args.get("sign")

        if not timestamp or not nonce or not sign:
            return {"content": "Invalid request."}, 400

        try:
            generator, mimetype = AttachmentImageService.get_image_preview(
                attachment_id, timestamp, nonce, sign
            )
        except _UnsupportedFileTypeError:
            raise UnsupportedFileTypeError()

        return Response(generator, mimetype=mimetype)


api.add_resource(ImagePreviewApi, "/files/<str:attachment_id>/image-preview")
