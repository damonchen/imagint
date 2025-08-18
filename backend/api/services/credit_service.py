import logging
from datetime import datetime, timedelta
from typing import Optional, List

from api.extensions.database import transaction
from api.data.models.credit import UserCredit, CreditTransaction
# from api.data.models.subscription import SubscriptionPlan
from api.data.models.user import User
from api.services.repository.user_repository import UserRepository
from api.services.repository.credit_repository import (
    UserCreditRepository,
    CreditTransactionRepository,
    SubscriptionPlanRepository,
)

logger = logging.getLogger(__name__)


class UserCreditService(object):
    """Credit系统服务类"""

    @staticmethod
    @transaction
    def initialize_user_credits(user: User) -> UserCredit:
        """为新注册用户初始化credit账户"""
        # 检查是否已有credit账户
        existing_credit = UserCreditRepository.get_user_credit(user.id)
        if existing_credit:
            return existing_credit

        # 创建新的credit账户，给予20个初始credit
        user_credit = UserCreditRepository.create_user_credit(
            user_id=user.id,
            balance=20,  # 注册时给予20个credit
            daily_credits_used=0,
            last_daily_reset=datetime.now(),
        )

        # 记录初始credit交易
        CreditTransactionRepository.create_credit_transaction(
            user_id=user.id,
            amount=20,
            balance_after=20,
            transaction_type="credit_add",
            source="registration_bonus",
            description="Welcome bonus for new user registration",
        )

        logger.info(f"Initialized credits for user {user.id}: 20 credits")
        return user_credit

    @staticmethod
    @transaction
    def add_subscription_credits(user: User, plan_name: str, amount_usd: int) -> bool:
        """为用户添加订阅计划的credit"""
        if not user.credit:
            user_credit = UserCreditService.initialize_user_credits(user)
        else:
            user_credit = user.credit

        # 根据价格确定credit数量
        credit_amount = 0
        if amount_usd == 1000:  # $10.00
            credit_amount = 500
        elif amount_usd == 2000:  # $20.00
            credit_amount = 1200
        else:
            logger.error(f"Invalid subscription amount: {amount_usd}")
            return False

        # 添加credit
        user_credit.add_credits(credit_amount, f"subscription_{plan_name}")

        # 记录订阅交易
        # CreditTransactionRepository.create_credit_transaction(
        #     user_id=user.id,
        #     amount=credit_amount,
        #     balance_after=user_credit.balance,
        #     transaction_type="credit_add",
        #     source=f"subscription_{plan_name}",
        #     description=f"Subscription plan: {plan_name} (${amount_usd/100:.2f})",
        # )

        logger.info(
            f"Added {credit_amount} credits for user {user.id} via {plan_name} subscription"
        )
        return True

    @staticmethod
    @transaction
    def consume_credits_for_image_generation(user: User, image_count: int = 1) -> bool:
        """消费credit生成图片"""
        if not user.credit:
            # 如果用户没有credit账户，先初始化
            user_credit = UserCreditService.initialize_user_credits(user)
        else:
            user_credit = user.credit

        # 检查是否有足够的credit
        if not user_credit.can_generate_image(image_count):
            logger.warning(
                f"User {user.id} insufficient credits for {image_count} images"
            )
            return False

        # 消费credit
        if user_credit.consume_credits(image_count):
            # 记录消费交易
            CreditTransactionRepository.create_credit_transaction(
                user_id=user.id,
                amount=-(image_count * 4),  # 负数表示消费
                balance_after=user_credit.balance,
                transaction_type="credit_consume",
                source="image_generation",
                description=f"Generated {image_count} image(s)",
            )

            logger.info(
                f"User {user.id} consumed {image_count * 4} credits for {image_count} images"
            )
            return True

        return False

    @staticmethod
    def get_user_transactions_pagination(user_id: int, page: int, per_page: int):
        return CreditTransactionRepository.get_user_transactions_pagination(
            user_id=user_id, page=page, per_page=per_page
        )

    @staticmethod
    def check_user_can_generate_image(user: User, image_count: int = 1) -> bool:
        """检查用户是否可以生成图片"""
        if not user.credit:
            return False
        return user.credit.can_generate_image(image_count)

    @staticmethod
    def get_user_credit_balance(user: User) -> int:
        """获取用户credit余额"""
        if not user.credit:
            return 0
        return user.credit.balance

    @staticmethod
    def get_user_credit_info(user: User) -> dict:
        """获取用户credit详细信息"""
        if not user.credit:
            return {
                "balance": 0,
                "daily_credits_used": 0,
                "can_generate": False,
                "images_remaining": 0,
            }

        credit = user.credit
        images_remaining = credit.balance // 4  # 每张图片需要4个credit

        return {
            "balance": credit.balance,
            "daily_credits_used": credit.daily_credits_used,
            "can_generate": credit.balance >= 4,
            "images_remaining": images_remaining,
            "last_daily_reset": (
                credit.last_daily_reset.isoformat() if credit.last_daily_reset else None
            ),
        }

    @staticmethod
    @transaction
    def process_daily_credit_reset():
        """处理每日credit重置（定时任务）"""
        now = datetime.now()
        user_credits = UserCreditRepository.get_user_credits()

        for user_credit in user_credits:
            user_credit.reset_daily_credits()

        logger.info(f"Processed daily credit reset for {len(user_credits)} users")

    @staticmethod
    def get_subscription_plans() -> List[dict]:
        """获取可用的订阅计划"""
        plans = SubscriptionPlanRepository.get_active_subscription_plans()

        def get_duration_days(plan):
            if plan.interval == 'monthly':
                return 30 * plan.interval_count
            elif plan.interval == 'yearly':
                return 360 * plan.interval_count

        return [
            {
                "id": plan.id,
                "name": plan.name,
                "price": plan.price,
                "price_display": f"${plan.price / 100:.2f}",
                "credit_amount": plan.credit_amount,
                "duration_days": get_duration_days(plan),
                "images_included": plan.credit_amount // 4,
            }
            for plan in plans
        ]
