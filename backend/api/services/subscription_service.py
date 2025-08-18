import json
import logging
from api.data.models.enums import OrderStatus, PaymentChannelStatus, SubscriptionStatus
from api.extensions.stripe import stripe
from api.services.errors.common import NotFoundError
from api.services.redis_service import RedisService
from api.services.repository.subscription_repository import (
    OrderRepository,
    SubscriptionRepository,
    SubscriptionPlanRepository,
)
from api.extensions.database import transaction

logger = logging.getLogger(__name__)


class SubscriptionPlanService(object):

    @staticmethod
    def load_plans():
        return SubscriptionPlanRepository.load_plans()

    @staticmethod
    def load_plan(plan_id):
        return SubscriptionPlanRepository.load_plan(plan_id)

    @staticmethod
    def get_plan_by_stripe_price_id(price_id):
        return SubscriptionPlanRepository.get_plan_by_stripe_price_id(price_id)

    @staticmethod
    def load_plan_by_name(name):
        return SubscriptionPlanRepository.load_plan_by_name(name)


class OrderService(object):

    @staticmethod
    def get_order(user, order_id):
        return OrderRepository.load_order(user, order_id)

    @staticmethod
    @transaction
    def create_order(user, subscription_id, payment_channel="stripe"):
        """Create a new order for subscription"""
        subscription = SubscriptionRepository.load_subscription(subscription_id)
        if not subscription:
            raise NotFoundError("Subscription not found")

        plan = SubscriptionPlanRepository.load_plan(subscription.plan_id)
        if not plan:
            raise NotFoundError("Plan not found")

        order = OrderRepository.create_order(
            user=user,
            subscription_id=subscription_id,
            amount=plan.price,
            discount_amount=0,
            payment_channel=payment_channel,
        )

        return order

    @staticmethod
    @transaction
    def cancel_order(user, order_id):
        """Cancel an order"""
        order = OrderRepository.load_order(user, order_id)
        if not order:
            raise NotFoundError("Order not found")

        return OrderRepository.cancel_order(user, order.trade_no)

    @staticmethod
    @transaction
    def refund_order(user, order_id):
        """Refund an order"""
        order = OrderRepository.load_order(user, order_id)
        if not order:
            raise NotFoundError("Order not found")

        if order.status != OrderStatus.PAID.value:
            raise NotFoundError("Order is not paid")

        # Cancel the order first
        order = OrderRepository.cancel_order(user, order.trade_no)

        # TODO: Implement refund logic with payment gateway

        return order

    @staticmethod
    @transaction
    def success_order(user, order_id):
        """Mark order as successful"""
        order = OrderRepository.load_order(user, order_id)
        if not order:
            raise NotFoundError("Order not found")

        return OrderRepository.pay_order(user, order.trade_no, order.amount)

    @staticmethod
    @transaction
    def fail_order(user, order_id):
        """Mark order as failed"""
        order = OrderRepository.load_order(user, order_id)
        if not order:
            raise NotFoundError("Order not found")

        return OrderRepository.expire_order(user, order.trade_no)

    @staticmethod
    @transaction
    def start_order(user, order_id, channel):
        """Start processing an order with specified payment channel"""
        order = OrderRepository.load_order(user, order_id)
        if not order:
            raise NotFoundError("Order not found")

        if order.status != OrderStatus.PENDING.value:
            raise NotFoundError("Order is not in pending status")

        # Update payment channel
        order = OrderRepository.update_order_status(
            order, user, "", payment_channel=channel
        )

        # TODO: Implement payment gateway integration

        return order

    @staticmethod
    def list_orders(user):
        return OrderRepository.load_orders(user)


class SubscriptionService(object):

    @staticmethod
    def load_subscription(subscription_id):
        return SubscriptionRepository.load_subscription(subscription_id)

    @staticmethod
    def create_new_subscription(user, plan, payment_channel):
        # 构建一笔订阅
        sub = SubscriptionService.create_subscription(user, plan, None)
        subscription_id = sub.id

        # 构建一笔订单
        order = OrderService.create_order(user, subscription_id, payment_channel=payment_channel)

        return sub, order

    @staticmethod
    def start_subscription(user, email, plan, app_web_url):
        plan = SubscriptionPlanService.load_plan_by_name(plan)
        if plan is None:
            return False, "no plan found"

        customer_id = RedisService.get(f"stripe:user:{user.id}")
        if not customer_id:
            # 创建Stripe客户
            customer = stripe.Customer.create(
                email=email,
                metadata={
                    "user_id": user.id,
                    "plan_id": plan.id,
                },
            )
            customer_id = customer.id

            RedisService.set(f"stripe:user:{user.id}", customer_id)

            sub, order = SubscriptionService.create_new_subscription(user, plan,
                                                                     payment_channel=PaymentChannelStatus.STRIPE)
            subscription_id = sub.id

            value = json.dumps({
                "user_id": user.id,
                "plan_id": plan.id,
                "subscription_id": subscription_id,
                "order_id": order.id,
            })
            RedisService.set(f"stripe:customer:{customer_id}", value.encode('utf-8'))
        else:
            customer_id = customer_id.decode('utf-8')
            value = RedisService.get(f"stripe:customer:{customer_id}")
            value = json.loads(value)
            subscription_id = value['subscription_id']

            subscription = SubscriptionService.load_subscription(subscription_id)

            print("subscription id ", subscription_id, subscription)
            # 如果状态不是active
            if subscription is None or subscription.status != SubscriptionStatus.ACTIVE:
                subscription, order = SubscriptionService.create_new_subscription(user, plan,
                                                                                  payment_channel=PaymentChannelStatus.STRIPE)
                subscription_id = subscription.id

                value = json.dumps({
                    "user_id": user.id,
                    "plan_id": plan.id,
                    "subscription_id": subscription_id,
                    "order_id": order.id,
                })
                RedisService.set(f"stripe:customer:{customer_id}", value.encode('utf-8'))

        price_id = plan.stripe_price_id
        logger.info("stripe customer %s %s", customer_id, price_id)

        # 创建订阅会话
        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url="%s/v1/stripe/success?session_id={CHECKOUT_SESSION_ID}"
                        % (app_web_url,),
            cancel_url=f"{app_web_url}/v1/stripe/cancel",
        )

        logger.info("create stripe session %s", session)

        RedisService.set(f"stripe:session:{session.id}", subscription_id, ex=600)

        return True, session

    @staticmethod
    @transaction
    def create_subscription(user, plan, stripe_subscription_id):
        """Create a new subscription for user"""
        subscription = SubscriptionRepository.create_subscription(
            user=user,
            plan=plan,
            stripe_subscription_id=stripe_subscription_id,
        )

        return subscription

    @staticmethod
    def update_subscription_stripe_id(subscription, stripe_subscription_id):
        return SubscriptionRepository.update_subscription_stripe_id(subscription, stripe_subscription_id)

    @staticmethod
    @transaction
    def active_subscription(user, subscription_id):
        return SubscriptionRepository.active_subscription(user, subscription_id)

    @staticmethod
    def expire_subscription(user, subscription_id):
        return SubscriptionRepository.expire_subscription(user, subscription_id)

    @staticmethod
    def list_subscriptions(user):
        """List all subscriptions for user"""
        return SubscriptionRepository.list_subscriptions(user)

    @staticmethod
    def cancel_subscription(user, subscription_id):
        """Cancel a subscription"""
        return SubscriptionRepository.cancel_subscription(
            user, subscription_id
        )

    @staticmethod
    def load_subscription_by_stripe_id(stripe_subscription_id):
        return SubscriptionRepository.load_subscription_by_stripe_id(
            stripe_subscription_id
        )
