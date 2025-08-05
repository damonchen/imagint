from datetime import datetime
from sqlalchemy.sql import func
from api.extensions.database import db
from api.utils.uuid import generate_db_id
from api.libs.helper import generate_string
from api.data.models.types import TimeStamp


class AppSetup(db.Model):
    __tablename__ = "app_setups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    version = db.Column(db.String(255), nullable=False)
    setup_at = db.Column(TimeStamp, nullable=False, server_default=func.now())


class OperationLog(db.Model):

    __tablename__ = "operation_logs"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="operation_log_pkey"),
        db.Index("operation_log_account_action_idx", "account_id", "action"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(255), nullable=False)
    payload = db.Column(db.Text, nullable=False)
    ip = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())


class ApiToken(db.Model):
    __tablename__ = "api_tokens"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="api_token_pkey"),
        db.Index("api_token_app_id_type_idx", "app_id", "type"),
        db.Index("api_token_token_idx", "token", "type"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_id = db.Column(db.Integer, nullable=True)
    type = db.Column(db.String(16), nullable=False)
    token = db.Column(db.String(255), nullable=False)

    created_by = db.Column(db.String(26), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_by = db.Column(db.String(26), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    @staticmethod
    def generate_api_key(prefix, n):
        while True:
            result = prefix + generate_string(n)
            while (
                db.session.query(ApiToken).filter(ApiToken.token == result).count() > 0
            ):
                result = prefix + generate_string(n)

            return result
