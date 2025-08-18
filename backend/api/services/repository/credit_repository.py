from api.data.models.credit import UserCredit, CreditTransaction
from api.data.models.subscription import SubscriptionPlan
from api.extensions.database import db
from datetime import datetime


class UserCreditRepository(object):
    @staticmethod
    def get_user_credit(user_id: int):
        return UserCredit.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_user_credits():
        return UserCredit.query.all()

    @staticmethod
    def create_user_credit(
        user_id: int, balance: int, daily_credits_used: int, last_daily_reset: datetime
    ):
        user_credit = UserCredit(
            user_id=user_id,
            balance=balance,
            daily_credits_used=daily_credits_used,
            last_daily_reset=last_daily_reset,
        )
        db.session.add(user_credit)
        db.session.flush()

        return user_credit

    @staticmethod
    def update_user_credit(user_id: int, credit: int):
        user_credit = UserCredit.query.filter_by(user_id=user_id).first()
        user_credit.credit = credit

        db.session.flush()

        return user_credit


class CreditTransactionRepository(object):
    @staticmethod
    def create_credit_transaction(
        user_id: int,
        amount: int,
        balance_after: int,
        transaction_type: str,
        source: str,
        description: str,
    ):
        credit_transaction = CreditTransaction(
            user_id=user_id,
            amount=amount,
            balance_after=balance_after,
            transaction_type=transaction_type,
            source=source,
            description=description,
        )

        db.session.add(credit_transaction)
        db.session.flush()

        return credit_transaction

    @staticmethod
    def get_user_transactions_pagination(user_id: int, page: int, per_page: int):
        return (
            CreditTransaction.query.filter_by(user_id=user_id)
            .order_by(CreditTransaction.created_at.desc())
            .paginate(page=page, per_page=per_page)
        )


class SubscriptionPlanRepository(object):
    @staticmethod
    def get_subscription_plans():
        return SubscriptionPlan.query.all()

    @staticmethod
    def get_active_subscription_plans():
        return SubscriptionPlan.query.filter_by(is_active=True).all()

    @staticmethod
    def get_subscription_plan(plan_id: int):
        return SubscriptionPlan.query.filter_by(id=plan_id).first()
