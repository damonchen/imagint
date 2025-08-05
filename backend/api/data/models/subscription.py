import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from sqlalchemy.types import DECIMAL
from sqlalchemy.sql import func

from api.extensions.database import db
from api.data.models.types import TimeStamp
from api.utils.uuid import generate_db_id, generate_db_trade_no
from api.data.models.enums import StrEnum


class PlanType(StrEnum):
    FREE = "free"
    PREMIUM = "premium"
    ULTRA = "ultra"


class Plan(db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(DECIMAL, nullable=False)
    discount_amount = db.Column(DECIMAL, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


class PlanFeature(db.Model):
    __tablename__ = "plan_features"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, nullable=False)
    feature = db.Column(
        db.String(255), nullable=False
    )  # 通常用类似 group.limit.count 这样的格式
    description = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, nullable=False, default=0)  # 排序

    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


class Subscription(db.Model):
    # 订阅信息

    __tablename__ = "subscriptions"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="subscription_pkey"),
        db.Index("subscription_account_idx", "account_id"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, nullable=False)
    plan_type = db.Column(db.String(26), nullable=False)  # 订阅类型， PlanType
    plan_id = db.Column(db.Integer, nullable=False)
    started_at = db.Column(
        TimeStamp, nullable=False, server_default=func.now()
    )  # 订阅起始时间
    ended_at = db.Column(
        TimeStamp, nullable=False, server_default=func.now()
    )  # 订阅结束时间
    status = db.Column(
        db.String(32), nullable=False, default="pending"
    )  # pending, active, expired, cancelled

    order_id = db.Column(db.String(26), nullable=False)  # 订单？

    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    def has_expired(self):
        now = datetime.now(datetime.UTC)
        return now > self.ended_at

    def is_nearest_expired(self, days=15):
        now = datetime.now(datetime.UTC)
        next = now + timedelta(days=days)
        return next > self.ended_at


# 订单信息
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    account_id = db.Column(db.Integer, nullable=False)
    subscription_id = db.Column(db.Integer, nullable=False)

    # 订单编号
    trade_no = db.Column(db.String(42), default=generate_db_trade_no)

    payment_channel = db.Column(db.String(32), nullable=True)  # 支付渠道

    # 订单金额
    amount = db.Column(DECIMAL, nullable=False)
    # 折扣费用
    discount_amount = db.Column(DECIMAL, nullable=False)
    # 支付金额
    paid_amount = db.Column(DECIMAL, nullable=False)

    # 订单状态
    status = db.Column(db.String(32), nullable=False, default="pending")
    payment_at = db.Column(TimeStamp, nullable=True)  # 支付时间

    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
