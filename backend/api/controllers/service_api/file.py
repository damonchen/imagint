import logging
import os
from flask import request, current_app, send_file
from flask_restful import marshal_with, abort
from werkzeug.datastructures.file_storage import FileStorage

from . import api
from api.controllers.common.errors import (
    FileTooLargeError,
    NoFileUploadedError,
    TooManayFilesError,
    UnsupportedFileTypeError,
)
from .wraps import WebApiResource

from api.data.fields.file_fields import list_attachment_file_fields
from api.services.errors.file import FileTooLargeError, UnsupportedFileTypeError
from api.services.attachment_service import AttachementService
from api.libs.url import get_file_url
from api.libs.decorator import unified_response
from api.libs.response import make_response

logger = logging.getLogger(__name__)


def get_attachment(file_id):
    """Return attachment file by file_id with proper mime type"""
    try:
        file = AttachementService.load_attachment_by_file_id(file_id)
        if not file:
            abort(404, message="File not found")

        # Check if file exists on disk
        if not os.path.exists(file.storage_path):
            abort(404, message="File not found")

        return send_file(
            file.storage_path,
            mimetype=file.mime_type,
            as_attachment=True,
            download_name=file.original_name,
        )

    except Exception as e:
        logger.error(f"Error getting attachment: {e}")
        abort(500, message="Internal server error")


class FileApi(WebApiResource):

    @unified_response(list_attachment_file_fields)
    def post(self, user):
        print("file upload api", request.files)
        if "files" not in request.files:
            return make_response(status="fail", message="No file uploaded")
            # raise NoFileUploadedError

        if len(request.files) > 1:
            return make_response(status="fail", message="Too many files uploaded")
            # raise TooManayFilesError()

        files = request.files["files"]
        temp_folder = current_app.config.get("UPLOAD_TEMP_FOLDER", "/tmp")

        print("files info is ", files)

        uploaded_files = []
        try:
            if isinstance(files, FileStorage):
                uploaded_file = AttachementService.upload_file(
                    user,
                    temp_folder,
                    files,
                )
                uploaded_files.append(uploaded_file)
            else:
                for file in files:
                    uploaded_file = AttachementService.upload_file(
                        user,
                        temp_folder,
                        file,
                    )
                    uploaded_files.append(uploaded_file)
        except FileTooLargeError as error:
            return make_response(status="fail", message=error.description)
            # raise FileTooLargeError(error.description)
        except UnsupportedFileTypeError:
            return make_response(status="fail", message="Unsupported file type")
            # raise UnsupportedFileTypeError()

        uploaded_files_with_url = []
        for file in uploaded_files:
            uploaded_files_with_url.append(
                {
                    "file_id": file.file_id,
                    "url": get_file_url(file.file_id),
                }
            )

        # Return a dictionary with items key to match the field definition
        return make_response(data={"items": uploaded_files_with_url})
        # return {
        #     'items': uploaded_files,
        # }
        # return uploaded_files, 201


class FileConfigApi(WebApiResource):

    def post(self, user, file_id):
        AttachementService.move_to_permanent(user, file_id)

        return make_response(
            data={"message": "File config updated", "status": "confirmed"}
        )


class FileCancelApi(WebApiResource):

    def post(self, user, file_id):
        AttachementService.delete_attachment(user, file_id)

        return make_response(
            data={"message": "File config updated", "status": "cancelled"}
        )


api.add_resource(FileApi, "/files/upload")
api.add_resource(FileConfigApi, "/files/confirm/<file_id>")
api.add_resource(FileCancelApi, "/files/cancel/<file_id>")
