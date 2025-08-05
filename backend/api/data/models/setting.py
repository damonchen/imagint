from datetime import datetime
from sqlalchemy.sql import func
from ...extensions.database import db
from api.utils.uuid import generate_db_id
from api.data.models.types import JSONType, TimeStamp


class Setting(db.Model):

    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, nullable=False)
    container_type = db.Column(db.String(26), nullable=False)
    key = db.Column(db.String(512), nullable=False)
    value = db.Column(JSONType)

    created_by = db.Column(db.String(26), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_by = db.Column(db.String(26), nullable=False)
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
