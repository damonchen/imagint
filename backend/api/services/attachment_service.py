import logging
import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Generator
from flask import current_app
from werkzeug.exceptions import NotFound
from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin

from api.core.file.attachment_image_parser import AttachmentImageParser
from api.data.models.attachment import Attachement
from api.extensions.storage import storage
from api.extensions.database import db
from api.services.repository.attachment_repository import AttachmentRepository
from api.services.errors.file import UnsupportedFileTypeError, FileTooLargeError
from api.libs.helper import digest
from api.extensions.database import transaction
from api.services.errors.common import NotFoundError


def allowed_file_extensions(filename):
    allowed_iamge_extensions = current_app.config.get("ALLOWED_IMAGE_EXTENSIONS")
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_iamge_extensions
    )


class AttachmentImageService(object):

    @staticmethod
    def get_image_preview(
        attachment_id: str, timestamp: str, nonce: str, sign: str
    ) -> tuple[Generator, str]:

        result = AttachmentImageParser.verify_image_preview(
            attachment_id, timestamp, nonce, sign
        )
        if not result:
            raise NotFound("File not found or signature is invalid")

        attachement = (
            db.session.query(Attachement)
            .filter(Attachement.id == attachment_id)
            .first()
        )

        if not attachement:
            raise NotFound("File not found or signature is invalid")

        if not attachement.is_image:
            raise UnsupportedFileTypeError()

        generator = storage.load(attachement.key, stream=True)

        return generator, attachement.mime_type

    @staticmethod
    def get_public_image_preview(attachment_id: str) -> tuple[Generator, str]:

        attachement = (
            db.session.query(Attachement)
            .filter(Attachement.id == attachment_id)
            .first()
        )

        if not attachement:
            raise NotFound("File not found or signature is invalid")

        if not attachement.is_image:
            raise UnsupportedFileTypeError()

        generator = storage.load(attachement.key)
        return generator, attachement.mime_type


class AttachementService(object):

    @staticmethod
    def disk_directory():
        now = datetime.now()
        return now.strftime("%Y/%m")

    @staticmethod
    def disk_filename(filename):
        now = datetime.now()
        current = now.strftime("%Y%m%d%H%M%S")
        return f"{current}_{filename}"

    @staticmethod
    def upload_file(
        user,
        folder,
        file,
    ):
        filename = secure_filename("".join(lazy_pinyin(file.filename)))
        if not allowed_file_extensions(filename):
            raise UnsupportedFileTypeError()

        file_size_limit = (
            current_app.config.get("UPLOAD_IMAGE_FILE_SIZE_LIMIT", 10) * 1024 * 1024
        )

        file_size = file.content_length
        if file_size > file_size_limit:
            raise FileTooLargeError()

        # data = file.read()
        content_type = file.content_type
        print(f"content type {content_type}")

        attachment = AttachementService.save_attachment(
            user,
            file,
            folder,
            file_size,
            content_type,
        )

        return attachment

    @staticmethod
    @transaction
    def save_attachment(user, file, folder, file_size, mime_type):

        file_id = str(uuid.uuid4())
        ext = os.path.splitext(file.filename)[1]
        temp_filename = f"{file_id}{ext}"
        temp_path = os.path.join(folder, temp_filename)

        file.save(temp_path)

        if file_size == 0:
            stat = os.stat(temp_path)
            file_size = stat.st_size

        attachment = AttachmentRepository.create_attachment(
            user,
            file_id,
            file.filename,
            temp_path,
            file_size,
            mime_type,
        )
        return attachment

    @staticmethod
    @transaction
    def move_to_permanent(user, file_id, perm_folder):
        """
        Move the attachment to the permanent folder.
        """
        attachment = AttachmentRepository.load_attachment_by_file_id(file_id)
        if attachment is None:
            raise NotFoundError("File not found")

        perm_filename = os.path.basename(attachment.storage_path)
        perm_path = os.path.join(perm_folder, perm_filename)
        os.rename(attachment.storage_path, perm_path)

        return AttachmentRepository.update_attachment(
            attachment,
            storage_path=perm_path,
            status="permanent",
            updated_by=user.id,
        )

    @staticmethod
    @transaction
    def delete_attachment(user, file_id):
        attachment = AttachmentRepository.load_attachment_by_file_id(file_id)
        if attachment is None:
            raise NotFoundError("File not found")

        return AttachmentRepository.update_attachment(
            attachment, status="to_delete", updated_by=user.id
        )

    @staticmethod
    def load_attachment(id):
        return AttachmentRepository.load_attachment(id)

    @staticmethod
    def load_attachment_by_file_id(file_id):
        return AttachmentRepository.load_attachment_by_file_id(file_id)

    @staticmethod
    def load_attachments_by_status(status, expiry_time=None):
        return AttachmentRepository.load_attachments_by_status(status, expiry_time)
