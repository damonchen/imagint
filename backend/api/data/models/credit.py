import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from api.extensions.database import db


class UserCredit(db.Model):
    __tablename__ = "user_credits"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    balance = Column(Integer, default=0, nullable=False)  # 当前credit余额
    daily_credits_used = Column(
        Integer, default=0, nullable=False
    )  # 今日已使用的免费credit
    last_daily_reset = Column(DateTime, default=datetime.now)  # 上次免费credit重置时间
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关联用户
    user = relationship("User", back_populates="credit")

    def can_generate_image(self, image_count: int = 1) -> bool:
        """检查用户是否有足够的credit生成图片"""
        required_credits = image_count * 4  # 每张图片需要4个credit
        return self.balance >= required_credits

    def consume_credits(self, image_count: int = 1) -> bool:
        """消费credit生成图片"""
        required_credits = image_count * 4
        if self.balance >= required_credits:
            self.balance -= required_credits
            self.daily_credits_used += required_credits
            return True
        return False

    def add_credits(self, amount: int, source: str = "purchase"):
        """添加credit"""
        self.balance += amount
        # 记录交易
        transaction = CreditTransaction(
            user_id=self.user_id,
            amount=amount,
            balance_after=self.balance,
            transaction_type="credit_add",
            source=source,
        )
        db.session.add(transaction)

    def reset_daily_credits(self):
        """重置每日免费credit"""
        now = datetime.now()
        if (now - self.last_daily_reset).days >= 1:
            self.daily_credits_used = 0
            self.last_daily_reset = now
            # 给免费用户发放每日credit
            if self.balance < 100:  # 如果余额少于100，认为是免费用户
                self.balance += 10
                transaction = CreditTransaction(
                    user_id=self.user_id,
                    amount=10,
                    balance_after=self.balance,
                    transaction_type="daily_bonus",
                    source="daily_free",
                )
                db.session.add(transaction)


class CreditTransaction(db.Model):
    __tablename__ = "credit_transactions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)  # credit数量（正数为增加，负数为减少）
    balance_after = Column(Integer, nullable=False)  # 交易后余额
    transaction_type = Column(
        String(32), nullable=False
    )  # credit_add, credit_consume, daily_bonus
    source = Column(
        String(64), nullable=False
    )  # purchase, subscription, daily_free, image_generation
    description = Column(Text, nullable=True)  # 交易描述
    created_at = Column(DateTime, default=datetime.now)

    # 关联用户
    user = relationship("User", back_populates="credit_transactions")


# class SubscriptionPlan(db.Model):
#     __tablename__ = "subscription_plans"
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = Column(String(64), nullable=False)  # 计划名称
#     stripe_price_id = Column(String(64), nullable=False)
#     price_usd = Column(Integer, nullable=False)  # 价格（美分）
#     credit_amount = Column(Integer, nullable=False)  # 包含的credit数量
#     duration_days = Column(Integer, nullable=False)  # 有效期（天）
#     is_active = Column(Boolean, default=True)  # 是否激活
#     created_at = Column(DateTime, default=datetime.now)
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         # 设置默认计划
#         if not self.name:
#             if self.price_usd == 0:
#                 self.name = "Free"
#                 self.credit_amount = 0
#                 self.duration_days = 30
#             elif self.price_usd == 1000:  # $10.00
#                 self.name = "Basic"
#                 self.credit_amount = 500
#                 self.duration_days = 30
#             elif self.price_usd == 2000:  # $20.00
#                 self.name = "Premium"
#                 self.credit_amount = 1200
#                 self.duration_days = 30
