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
    PRO = "pro"
    ULTRA = "ultra"


class SubscriptionPlan(db.Model):
    __tablename__ = "subscription_plans"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)  # 计划名称, free, pro, ultra
    description = db.Column(db.Text, nullable=True)  # 计划的描述内容，用markdown描述
    stripe_price_id = db.Column(db.String(64), nullable=False)
    interval = db.Column(db.String(32), nullable=False, default='monthly')  # 计费周期，默认是30天, monthly, quarterly, yearly
    interval_count = db.Column(db.Integer, nullable=False, default=1)  # 计费周期数，比如1或者12，发放的频率是按照月来发放的
    price = db.Column(db.Integer, nullable=False)  # 价格（美分）
    credit_amount = db.Column(db.Integer, nullable=False)  # 包含的credit数量
    is_active = db.Column(db.Boolean, default=True)  # 是否激活

    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


# 一个人可以订阅多次，每次订阅一个月，要允许是否自动续订，如果是自动续订的
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

    stripe_subscription_id = db.Column(db.String(128), nullable=True)
    started_at = db.Column(
        TimeStamp, nullable=False, server_default=func.now()
    )  # 订阅起始时间
    ended_at = db.Column(
        TimeStamp, nullable=False, server_default=func.now()
    )  # 订阅结束时间
    status = db.Column(
        db.String(32), nullable=False, default="unpaid"
    )  # unpaid, active, expired, cancelled
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

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def is_unpaid(self):
        return self.status == 'unpaid'

    @property
    def is_cancelled(self):
        return self.status == 'cancelled'


# 订单信息
class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, nullable=False)
    subscription_id = db.Column(db.Integer, nullable=False)

    # 下单时间
    order_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    payment_channel = db.Column(db.String(16), nullable=False, default="stripe")  # 支付通道，默认采用stripe
    total_amount = db.Column(DECIMAL, nullable=False)  # 订单总金额
    discount_amount = db.Column(DECIMAL, nullable=True)  # 折扣金额
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
