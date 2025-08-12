from sqlalchemy import DECIMAL
from sqlalchemy.sql import func
from api.extensions.database import db
from api.data.models.types import TimeStamp
from decimal import Decimal


# 发票，不可修改，暂时不开发
class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    period_start = db.Column(TimeStamp, nullable=False)
    period_end = db.Column(TimeStamp, nullable=False)
    amount_due = db.Column(DECIMAL, nullable=False)  # 应付金额
    amount_paid = db.Column(DECIMAL, nullable=False)  # 已付金额
    status = db.Column(
        db.String(32), nullable=False, default="unpaid"
    )  # unpaid, paid, overdue

    payment_due_date = db.Column(TimeStamp, nullable=False)  # 最晚支付日期

    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())


# 使用记录
class UsageRecord(db.Model):
    __tablename__ = "usage_records"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    usage_at = db.Column(
        TimeStamp, nullable=False, server_default=func.now()
    )  # 使用日期
    tokens_used = db.Column(db.Integer, nullable=False, default=0)  # 使用的令牌数
    requests_made = db.Column(db.Integer, nullable=False, default=0)  # 当天调用次数
    cost = db.Column(DECIMAL, nullable=False, default=Decimal("0.00"))  # 当天费用

    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


class Refund(db.Model):
    __tablename__ = "refunds"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    payment_order_id = db.Column(db.Integer, nullable=False)  # 关联的支付订单ID
    amount = db.Column(DECIMAL, nullable=False)  # 退款金额
    currency = db.Column(db.String(16), nullable=False, default="USD")  # 货币类型
    status = db.Column(
        db.String(32), nullable=False, default="pending"
    )  # 退款状态，如 pending, processed, failed
    gateway_refund_id = db.Column(db.String(255), nullable=True)  # 支付网关的退款ID
    reason = db.Column(db.String(255), nullable=True)  # 退款原因

    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, nullable=True)  # 订单，可空，依据refund来定义
    type = db.Column(
        db.String(32), nullable=False
    )  # 交易类型，如 recharge, payment, refund，adjustment
    amount = db.Column(DECIMAL, nullable=False)  # 交易金额
    currency = db.Column(db.String(16), nullable=False, default="USD")  # 货币类型

    status = db.Column(
        db.String(32), nullable=False, default="pending"
    )  # 交易状态，如 pending,processing,success,failed,expired,cancelled,refunded

    payment_channel = db.Column(
        db.String(32), nullable=True
    )  # 支付渠道, paypal, alipay, wechat, stripe, etc.
    reference_id = db.Column(
        db.String(64), nullable=True
    )  # 参考编号，如支付平台的交易号

    description = db.Column(db.String(255), nullable=True)  # 交易描述
    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
