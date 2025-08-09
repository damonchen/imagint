import logging
import os
from flask import request, current_app, send_file, abort
from flask_restful import marshal_with
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

logger = logging.getLogger(__name__)


def get_attachment(file_id):
    """Return attachment file by file_id with proper mime type"""
    try:
        file = AttachementService.load_attachment_by_file_id(file_id)
        if not file:
            abort(404)

        # Check if file exists on disk
        if not os.path.exists(file.storage_path):
            abort(404)

        return send_file(
            file.storage_path,
            mimetype=file.mime_type,
            as_attachment=True,
            download_name=file.original_name,
        )

    except Exception as e:
        logger.error(f"Error getting attachment: {e}")
        abort(500)


class FileApi(WebApiResource):

    @marshal_with(list_attachment_file_fields)
    def post(self, account):
        print("file upload api", request.files)
        if "files" not in request.files:
            raise NoFileUploadedError

        if len(request.files) > 1:
            raise TooManayFilesError()

        files = request.files["files"]
        temp_folder = current_app.config.get("UPLOAD_TEMP_FOLDER", "/tmp")

        print("files info is ", files)

        uploaded_files = []
        try:
            if isinstance(files, FileStorage):
                uploaded_file = AttachementService.upload_file(
                    account,
                    temp_folder,
                    files,
                )
                uploaded_files.append(uploaded_file)
            else:
                for file in files:
                    uploaded_file = AttachementService.upload_file(
                        account,
                        temp_folder,
                        file,
                    )
                    uploaded_files.append(uploaded_file)
        except FileTooLargeError as error:
            raise FileTooLargeError(error.description)
        except UnsupportedFileTypeError:
            raise UnsupportedFileTypeError()

        uploaded_files_with_url = []
        for file in uploaded_files:
            uploaded_files_with_url.append(
                {
                    "file_id": file.file_id,
                    "url": get_file_url(file.file_id),
                }
            )

        # Return a dictionary with items key to match the field definition
        return {"items": uploaded_files_with_url}
        # return {
        #     'items': uploaded_files,
        # }
        # return uploaded_files, 201


class FileConfigApi(WebApiResource):

    def post(self, account, file_id):
        AttachementService.move_to_permanent(account, file_id)

        return {"message": "File config updated", "status": "confirmed"}, 200


class FileCancelApi(WebApiResource):

    def post(self, account, file_id):
        AttachementService.delete_attachment(account, file_id)

        return {"message": "File config updated", "status": "cancelled"}, 200


api.add_resource(FileApi, "/files/upload")
api.add_resource(FileConfigApi, "/files/confirm/<file_id>")
api.add_resource(FileCancelApi, "/files/cancel/<file_id>")
