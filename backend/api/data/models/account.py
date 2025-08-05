from validator_collection import validators
from sqlalchemy import DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from datetime import datetime
from ...extensions.database import db
from ...data.models.types import JSONType, TimeStamp
from ...utils.uuid import generate_db_id
from ...data.models.enums import (
    AccountStatus,
)
from ...libs.password import hash_password, generate_password_salt, compare_password

SYSTEM_ACCOUNT_ID = "01HVEHYVN0KB600CBHM6ZGM3MH"


class Account(db.Model):
    __tablename__ = "accounts"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="account_pkey"),
        db.Index("idx_account_email", "email"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=True)  # 邮箱登录的邮箱
    salt = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(255), nullable=True)  # 邮箱登录的密码

    google_account_id = db.Column(db.String(26), nullable=True)  # google的oauth2.0 id

    username = db.Column(
        db.String(255), nullable=False, default=""
    )  # 姓名，便于在页面上展示
    avatar = db.Column(db.String(1024))
    status = db.Column(db.String(26), nullable=False, default="pending")
    option = db.Column(JSONType)

    language = db.Column(db.String(26), nullable=False, default="zh-CN")
    theme = db.Column(db.String(16), nullable=False, default="light")
    timezone = db.Column(db.String(26), nullable=False, default="Asia/Shanghai")

    invited_by = db.Column(db.Integer, nullable=True)

    last_login_at = db.Column(TimeStamp)
    created_at = db.Column(TimeStamp, server_default=func.now())
    updated_at = db.Column(
        TimeStamp,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    def set_password(self, password):
        """Set password with auto-generated salt for the account."""
        salt = generate_password_salt()
        self.salt = salt
        self.password = hash_password(password, bytes.fromhex(salt))

    def check_password(self, password):
        """Check if provided password matches stored hash."""
        return compare_password(password, self.password, self.salt)

    def change_password(self, current_password, new_password):
        """Change password after verifying current password."""
        if not self.check_password(current_password):
            return False
        self.set_password(new_password)
        return True

    @property
    def is_active(self):
        return self.status == AccountStatus.ACTIVE.value

    @property
    def is_banned(self):
        return self.status == AccountStatus.BANNED.value

    @property
    def is_closed(self):
        return self.status == AccountStatus.CLOSED.value

    @property
    def is_not_valid(self):
        return self.is_banned or self.is_closed


class AccountPasswordToken(db.Model):
    __tablename__ = "account_password_tokens"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="account_password_token_pkey"),
        db.Index("idx_account_password_token_account_id", "account_id"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, nullable=False)
    type = db.Column(
        db.String(32), nullable=False
    )  # token type, as reset, mail_validate, etc.
    token = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(TimeStamp, nullable=False)
    created_at = db.Column(TimeStamp, server_default=func.now())
    updated_at = db.Column(
        TimeStamp,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    @property
    def is_expired(self):
        return self.expires_at < datetime.now(datetime.UTC)


class GoogleAccount(db.Model):
    __tablename__ = "google_accounts"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="google_account_pkey"),
        db.Index("idx_google_account_email", "email"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), nullable=False)  # google email address
    nickname = db.Column(db.String(256), nullable=True)
    avatar = db.Column(db.String(1024))
    google_account_id = db.Column(db.String(26), nullable=False)  # google中的account id

    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(TimeStamp, server_default=func.now())
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        TimeStamp,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    @validates("email")
    def validate_email(self, key, field):
        return validators.email(field)

    @property
    def is_valid(self):
        return self.email is not None and self.email != ""
