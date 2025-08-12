import logging
import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy.types import DECIMAL
from sqlalchemy.sql import func

from api.extensions.database import db
from api.data.models.types import TimeStamp
from api.utils.uuid import generate_db_id, generate_db_trade_no
from api.data.models.enums import StrEnum

from api.data.models.types import JSONType


class PlanType(StrEnum):
    FREE = "free"
    PREMIUM = "premium"
    ULTRA = "ultra"


class Plan(db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    monthly_fee = db.Column(DECIMAL, nullable=False)  # 月费用
    included_tokens = db.Column(db.Integer, nullable=False)  # 包含的令牌数
    included_requests = db.Column(db.Integer, nullable=False)  # 包含的请求数
    concurrency_limit = db.Column(db.Integer, nullable=False)  # 并发限制
    extra_token_price = db.Column(DECIMAL, nullable=False)  # 超出令牌数的价格
    extra_request_price = db.Column(DECIMAL, nullable=False)  # 超出请求
    feature = db.Column(JSONType, nullable=True)  # 特性描述，通常是 JSON 字符串

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
        db.Index("subscription_user_idx", "user_id"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    plan_id = db.Column(db.Integer, nullable=False)

    started_at = db.Column(
        TimeStamp, nullable=False, server_default=func.now()
    )  # 订阅起始时间
    ended_at = db.Column(
        TimeStamp, nullable=False, server_default=func.now()
    )  # 订阅结束时间
    status = db.Column(
        db.String(32), nullable=False, default="active"
    )  # active, expired, cancelled
    auto_renew = db.Column(db.Boolean, nullable=False, default=True)  # 是否自动续订

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
        now = datetime.datetime.now(datetime.UTC)
        return now > self.ended_at

    def is_nearest_expired(self, days=15):
        now = datetime.datetime.now(datetime.UTC)
        next = now + datetime.timedelta(days=days)
        return next > self.ended_at


# 订单信息
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, nullable=False)
    subscription_id = db.Column(db.Integer, nullable=False)

    # 下单时间
    order_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    total_amount = db.Column(DECIMAL, nullable=False)  # 订单总金额
    currency = db.Column(db.String(16), nullable=False, default="USD")  # 货币类型
    tax_rate = db.Column(DECIMAL(5, 2), nullable=False, default=0.0)  # 税率
    status = db.Column(
        db.String(32), nullable=False, default="pending"
    )  # pending, confirmed, processing, shipped, completed, cancelled, refunded

    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
