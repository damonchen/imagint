import datetime
from dateutil.relativedelta import relativedelta
import logging
from api.data.models.enums import SubscriptionStatus, OrderStatus
from api.data.models.subscription import Subscription, Plan, Order
from api.extensions.database import db
from api.events.subscription import *

from api.services.errors.common import NotFoundError, NotPermittedError


class PlanRepository(object):

    @staticmethod
    def load_plan(plan_id):
        return db.session.query(Plan).filter(Plan.id == plan_id).first()

    @staticmethod
    def load_plan_by_name(name):
        return db.session.query(Plan).filter(Plan.name == name).first()


class SubscriptionRepository(object):

    @staticmethod
    def list_subscriptions(account, status=SubscriptionStatus.ACTIVE.value):
        return (
            db.session.query(Subscription)
            .filter(Subscription.account_id == account.id, Subscription.status == status)
            .all()
        )

    @staticmethod
    def load_subscription(subscription_id, status=SubscriptionStatus.ACTIVE.value):
        return (
            db.session.query(Subscription)
            .filter(Subscription.id == subscription_id, Subscription.status == status)
            .first()
        )

    @staticmethod
    def create_subscription(account, plan, status=SubscriptionStatus.ACTIVE.value):
        now = datetime.datetime.now(datetime.UTC)
        ended_at = now = relativedelta(months=+plan.month)

        subscription = Subscription(
            account_id=account.id,
            plan_id=plan.id,
            plan_type=plan.type,
            started_at=now,
            ended_at=ended_at,
            status=status,
            created_by=account.id,
            updated_by=account.id,
        )
        db.session.add(subscription)
        db.session.flush()

        subscription_was_created.send(subscription)

        return subscription

    @staticmethod
    def update_subscription(
        account,
        subscription_id,
        plan_id=None,
        status=None,
    ):
        subscription = SubscriptionRepository.load_subscription(
            subscription_id, status=SubscriptionStatus.ACTIVE.value
        )
        if subscription is None:
            raise NotFoundError("subscription not found")

        if subscription.account_id != account.id:
            raise NotPermittedError("subscription not permitted")

        if plan_id is not None:
            plan = PlanRepository.load_plan(plan_id=plan_id)
            if plan is None:
                raise NotFoundError("plan not found")

            subscription.plan_id = plan_id
            subscription.started_at = datetime.datetime.now(datetime.UTC)
            subscription.ended_at = datetime.datetime.now(datetime.UTC) + relativedelta(
                months=+plan.month
            )

        if status is not None:
            subscription.status = status

        subscription.updated_by = account.id

        db.session.add(subscription)
        db.session.flush()

        return subscription

    @staticmethod
    def active_subscription(account, subscription_id):
        status = SubscriptionStatus.ACTIVE.value
        return SubscriptionRepository.update_subscription(
            account, subscription_id, status
        )

    @staticmethod
    def pasue_subscription(account, subscription_id):
        status = SubscriptionStatus.PAUSED.value
        return SubscriptionRepository.update_subscription(
            account, subscription_id, status
        )

    @staticmethod
    def cancel_subscription(account, subscription_id):
        status = SubscriptionStatus.CANCELLED.value
        return SubscriptionRepository.update_subscription(
            account, subscription_id, status
        )

    @staticmethod
    def expire_subscription(account, subscription_id):
        status = SubscriptionStatus.EXPIRED.value
        return SubscriptionRepository.update_subscription(
            account, subscription_id, status
        )


class OrderRepository(object):

    @staticmethod
    def create_order(
        account, subscription_id, amount, discount_amount=0, payment_channel=""
    ):
        subscription = SubscriptionRepository.load_subscription(
            subscription_id=subscription_id
        )
        if subscription is None:
            raise NotFoundError()

        order = Order(
            account_id=account.id,
            subscription_id=subscription.id,
            amount=amount,
            discount_amount=discount_amount,
            payment_channel=payment_channel,
            status=OrderStatus.PENDING.value,
            created_by=account.id,
            udpated_by=account.id,
        )
        db.session.add(order)
        db.session.flush()

        return order

    @staticmethod
    def load_order_by_trade_no(trade_no):
        return db.session.query(Order).filter(Order.trade_no == trade_no).first()

    @staticmethod
    def load_order(order_id):
        return db.session.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def load_order_by_subscription_id(subscription_id):
        return (
            db.session.query(Order)
            .filter(Order.subscription_id == subscription_id)
            .first()
        )

    @staticmethod
    def pay_order(account, trade_no, paid_amount):
        order = OrderRepository.load_order_by_trade_no(trade_no)
        if order is None:
            raise NotFoundError()

        order.status = OrderStatus.PAID.value
        order.paid_amount = paid_amount
        order.payment_at = datetime.datetime.now(datetime.UTC)
        order.updated_by = account.id

        db.session.add(order)
        db.session.flush()

        return order

    @staticmethod
    def cancel_order(account, trade_no):
        order = OrderRepository.load_order_by_trade_no(trade_no)
        if order is None:
            raise NotFoundError()

        order.status = OrderStatus.CANCELLED.value
        order.updated_by = account.id

        db.session.add(order)
        db.session.flush()

        return order

    @staticmethod
    def expire_order(account, trade_no):
        order = OrderRepository.load_order_by_trade_no(trade_no)
        if order is None:
            raise NotFoundError()

        order.status = OrderStatus.EXPIRED.value
        order.updated_by = account.id

        db.session.add(order)
        db.session.flush()

        return order

    @staticmethod
    def update_order_status(
        order, account, status, paid_amount=None, payment_channel=None
    ):
        order.status = status
        order.updated_by = account.id

        if paid_amount is not None:
            order.paid_amount = paid_amount
            order.payment_at = datetime.datetime.now(datetime.UTC)

        if status == OrderStatus.CANCELLED.value:
            order.payment_at = None
            order.paid_amount = None

        if payment_channel is not None:
            order.payment_channel = payment_channel

        db.session.add(order)
        db.session.flush()

        return order
