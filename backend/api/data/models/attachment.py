from datetime import datetime
from sqlalchemy.sql import func
from api.extensions.database import db
from api.data.models.types import TimeStamp
from api.utils.uuid import generate_db_id


class Attachement(db.Model):

    __tablename__ = "attachments"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="attachment_pkey"),
        db.Index("attachment_file_id_idx", "file_id"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_id = db.Column(db.String(128), nullable=False)
    account_id = db.Column(db.Integer, nullable=True)
    original_name = db.Column(db.String(1024), nullable=False)
    storage_path = db.Column(db.String(1024), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(32), nullable=False)
    digest = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(32), nullable=False
    )  # 'temp' or 'permanent' or 'to_delete'

    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(TimeStamp, server_default=func.now())
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    @property
    def extension(self):
        return self.original_name.split(".")[-1]

    @property
    def length(self):
        return self.file_size

    @property
    def size(self):
        return self.file_size

    @property
    def name(self):
        return self.original_name

    @property
    def is_image(self):
        return self.mime_type in [
            "image/bmp",
            "image/png",
            "image/jpg",
            "image/jpeg",
            "image/gif",
            "image/svg+xml",
            "image/webp",
        ]
