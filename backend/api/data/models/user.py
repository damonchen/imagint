from validator_collection import validators
from sqlalchemy import DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from datetime import datetime
from ...extensions.database import db
from ...data.models.types import JSONType, TimeStamp
from ...utils.uuid import generate_db_id
from ...data.models.enums import (
    UserStatus,
)
from ...libs.password import hash_password, generate_password_salt, compare_password

SYSTEM_USER_ID = "01HVEHYVN0KB600CBHM6ZGM3MH"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(1024))
    status = db.Column(
        db.String(26), nullable=False, default="active"
    )  # active, inactive, banned
    option = db.Column(JSONType)
    salt = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)  # 邮箱登录的密码
    role = db.Column(db.String(26), nullable=False, default="user")  # "user" or "admin"

    subscription_status = db.Column(
        db.String(26), nullable=False, default="inactive"
    )  # 是否订阅状态

    invited_by = db.Column(db.Integer, nullable=True)
    timezone = db.Column(db.String(255), nullable=False, default="Asia/Shanghai")
    theme = db.Column(db.String(255), nullable=False, default="light")

    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    # Credit relationships
    credit = db.relationship("UserCredit", back_populates="user", uselist=False)
    credit_transactions = db.relationship("CreditTransaction", back_populates="user")

    def set_password(self, password):
        """Set password with auto-generated salt for the user."""
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
        return self.status == UserStatus.ACTIVE.value

    @property
    def is_banned(self):
        return self.status == UserStatus.BANNED.value

    @property
    def is_closed(self):
        return self.status == UserStatus.CLOSED.value

    @property
    def is_not_valid(self):
        return self.is_banned or self.is_closed

    def get_credit_balance(self):
        """获取用户credit余额"""
        if not self.credit:
            return 0
        return self.credit.balance

    def can_generate_image(self, image_count: int = 1) -> bool:
        """检查用户是否有足够的credit生成图片"""
        if not self.credit:
            return False
        return self.credit.can_generate_image(image_count)

    def consume_credits_for_image(self, image_count: int = 1) -> bool:
        """消费credit生成图片"""
        if not self.credit:
            return False
        return self.credit.consume_credits(image_count)


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    balance = db.Column(
        DECIMAL(precision=10, scale=2),
        nullable=False,
        default=0.00,
    )  # 账户余额
    currency = db.Column(
        db.String(16),
        nullable=False,
        default="USD",
    )  # 账户货币类型
    total_spent = db.Column(
        DECIMAL(precision=10, scale=2),
        nullable=False,
        default=0.00,
    )  # 总消费金额
    total_recharge = db.Column(
        DECIMAL(precision=10, scale=2),
        nullable=False,
        default=0.00,
    )  # 总充值金额
    last_transaction_at = db.Column(
        TimeStamp,
        nullable=True,
    )  # 最后一次交易时间
    created_at = db.Column(TimeStamp, server_default=func.now())
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


class UserPasswordToken(db.Model):
    __tablename__ = "user_password_tokens"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="user_password_token_pkey"),
        db.Index("idx_user_password_token_user_id", "user_id"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
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


class GoogleUser(db.Model):
    __tablename__ = "google_users"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="google_user_pkey"),
        db.Index("idx_google_user_email", "email"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), nullable=False)  # google email address
    nickname = db.Column(db.String(256), nullable=True)
    avatar = db.Column(db.String(1024))
    google_user_id = db.Column(db.String(26), nullable=False)  # google中的user id

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


class UserLocationEvidence(db.Model):
    __tablename__ = "user_location_evidences"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    type = db.Column(
        db.String(50), nullable=False
    )  # 证据类型，如 ip, gps, phone, billing_address, payment_country, etc.
    data = db.Column(JSONType, nullable=False)  # 证据数据

    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
