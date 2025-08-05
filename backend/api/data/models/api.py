import enum
from sqlalchemy.sql import func
from ...libs.language import LanguageEnumValue
from ...extensions.database import db
from ...data.models.types import TimeStamp
from ...utils.uuid import generate_db_id


class Webhook(db.Model):

    __tablename__ = "webhooks"

    id = db.Column(db.String(26), primary_key=True, default=generate_db_id)
    user_id = db.Column(db.String(26), nullable=False)
    event = db.Column(db.String(255), nullable=False)

    created_by = db.Column(db.String(26), nullable=False)
    created_at = db.Column(TimeStamp, server_default=func.now())
    updated_by = db.Column(db.String(26), nullable=False)
    updated_at = db.Column(
        TimeStamp,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
