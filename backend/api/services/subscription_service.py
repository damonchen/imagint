from api.data.models.enums import OrderStatus
from api.services.errors.common import NotFoundError
from api.services.repository.subscription_repository import (
    OrderRepository,
    SubscriptionRepository,
    PlanRepository,
)
from api.extensions.database import transaction


class SubscriptionService(object):
    @staticmethod
    @transaction
    def create_subscription(account, plan_id):
        """Create a new subscription for account"""
        plan = PlanRepository.load_plan(plan_id)
        if not plan:
            raise NotFoundError("Plan not found")

        subscription = SubscriptionRepository.create_subscription(
            account=account,
            plan=plan,
        )

        return subscription

    @staticmethod
    def list_subscriptions(account):
        """List all subscriptions for account"""
        return SubscriptionRepository.list_subscriptions(account)

    @staticmethod
    def load_subscription(subscription_id):
        """Load a subscription by ID"""
        return SubscriptionRepository.load_subscription(subscription_id)


class OrderService(object):
    @staticmethod
    @transaction
    def create_order(account, subscription_id, payment_channel):
        """Create a new order for subscription"""
        subscription = SubscriptionRepository.load_subscription(subscription_id)
        if not subscription:
            raise NotFoundError("Subscription not found")

        plan = PlanRepository.load_plan(subscription.plan_id)
        if not plan:
            raise NotFoundError("Plan not found")

        order = OrderRepository.create_order(
            account=account,
            subscription_id=subscription_id,
            amount=plan.price,
            discount_amount=plan.discount_amount,
            payment_channel=payment_channel,
        )

        return order

    @staticmethod
    @transaction
    def cancel_order(account, order_id):
        """Cancel an order"""
        order = OrderRepository.load_order(order_id)
        if not order:
            raise NotFoundError("Order not found")

        return OrderRepository.cancel_order(account, order.trade_no)

    @staticmethod
    @transaction
    def refund_order(account, order_id):
        """Refund an order"""
        order = OrderRepository.load_order(order_id)
        if not order:
            raise NotFoundError("Order not found")

        if order.status != OrderStatus.PAID.value:
            raise NotFoundError("Order is not paid")

        # Cancel the order first
        order = OrderRepository.cancel_order(account, order.trade_no)

        # TODO: Implement refund logic with payment gateway

        return order

    @staticmethod
    @transaction
    def success_order(account, order_id):
        """Mark order as successful"""
        order = OrderRepository.load_order(order_id)
        if not order:
            raise NotFoundError("Order not found")

        return OrderRepository.pay_order(account, order.trade_no, order.amount)

    @staticmethod
    @transaction
    def fail_order(account, order_id):
        """Mark order as failed"""
        order = OrderRepository.load_order(order_id)
        if not order:
            raise NotFoundError("Order not found")

        return OrderRepository.expire_order(account, order.trade_no)

    @staticmethod
    @transaction
    def start_order(account, order_id, channel):
        """Start processing an order with specified payment channel"""
        order = OrderRepository.load_order(order_id)
        if not order:
            raise NotFoundError("Order not found")

        if order.status != OrderStatus.PENDING.value:
            raise NotFoundError("Order is not in pending status")

        # Update payment channel
        order = OrderRepository.update_order_status(
            order, account, payment_channel=channel
        )

        # TODO: Implement payment gateway integration

        return order
