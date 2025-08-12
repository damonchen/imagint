import logging
import uuid
from datetime import datetime
from api.extensions.database import db
from api.data.models.attachment import Attachement
from api.services.errors.common import NotFoundError
from api.libs.helper import digest_file

logger = logging.getLogger("services.attachment")


class AttachmentRepository(object):

    @staticmethod
    def load_attachment(attachment_id):
        if isinstance(attachment_id, Attachement):
            return attachment_id

        attachment = Attachement.query.filter_by(id=attachment_id).first()
        if attachment is None:
            raise NotFoundError("Attachment not found")

        return attachment

    @staticmethod
    def load_attachment_by_file_id(file_id):
        attachment = Attachement.query.filter_by(file_id=file_id).first()
        if attachment is None:
            raise NotFoundError("Attachment not found")
        return attachment

    @staticmethod
    def load_attachments_by_file_ids(file_ids):
        attachments = Attachement.query.filter_by(
            Attachement.file_id.in_(file_ids)
        ).all()
        return attachments

    @staticmethod
    def create_attachment(
        user,
        file_id,
        original_name,
        storage_path,
        file_size,
        mime_type,
        description=None,
        status="temp",
        created_by=None,
    ) -> Attachement:

        digest = digest_file(storage_path)

        attachment = Attachement(
            file_id=file_id,
            user_id=user.id,
            original_name=original_name,
            storage_path=storage_path,
            file_size=file_size,
            mime_type=mime_type,
            digest=digest,
            description=description,
            status=status,
            created_by=created_by or user.id,
            updated_by=created_by or user.id,
        )

        db.session.add(attachment)
        db.session.flush()

        return attachment

    @staticmethod
    def update_attachment(attachment, **kwargs) -> Attachement:
        for key, value in kwargs.items():
            setattr(attachment, key, value)

        db.session.add(attachment)
        db.session.flush()
        return attachment

    @staticmethod
    def load_attachments_by_status(status, expiry_time=None):
        query = Attachement.query.filter_by(status=status)
        if expiry_time is not None:
            query = query.filter(Attachement.created_at < expiry_time)
        return query.all()

    @staticmethod
    def delete_attachment(attachment):
        db.session.delete(attachment)
        db.session.flush()
