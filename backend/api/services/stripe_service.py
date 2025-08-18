import json

from api.events.subscription import subscription_stripe_id_updated
from api.extensions.database import transaction
from api.services.redis_service import RedisService
from api.services.user_service import UserService
from api.services.credit_service import UserCreditService
from api.services.subscription_service import (
    SubscriptionService,
    SubscriptionPlanService,
)


def get_customer_subscription(customer_id):
    value = RedisService.get(f"stripe:customer:{customer_id}")
    value = json.loads(value)
    return value['subscription_id']


class StripeService(object):

    # 事件处理函数示例
    @staticmethod
    @transaction
    def handle_subscription_created(subscription, payload):
        print(f"New subscription created: {subscription.id}, {payload}")
        stripe_subscription_id = subscription["id"]

        customer_id = subscription['customer']
        subscription_id = get_customer_subscription(customer_id=customer_id)

        # user_id = value['user_id']
        # user = UserService.load_user(user_id)
        #
        # plan_id = value['plan_id']
        # plan = SubscriptionPlanService.load_plan(plan_id)

        # subscription_id = value['subscription_id']
        subscription = SubscriptionService.load_subscription(subscription_id)

        SubscriptionService.update_subscription_stripe_id(
            subscription, stripe_subscription_id
        )

        subscription_stripe_id_updated.send(
            json.dumps({'id': subscription_id, 'stripe_subscription_id': stripe_subscription_id, }))

    @staticmethod
    @transaction
    def handle_subscription_updated(subscription, payload):
        print(f"Subscription updated: {subscription.id}, {payload}")
        # 在这里更新数据库（例如将用户标记为订阅状态）
        # user_id = int(subscription["metadata"]["user_id"])
        # user = UserService.load_user(user_id)
        # if not user:
        #     return

        # # 此处更新实际的订阅信息
        # UserService.update_user_subscription(user, subscription)

        # # 更新订阅信息
        # SubscriptionService.update_subscription(user, subscription, payload)

    @staticmethod
    @transaction
    def handle_payment_succeeded(invoice, payload):
        customer_id = invoice['customer']
        subscription_id = get_customer_subscription(customer_id=customer_id)
        subscription = SubscriptionService.load_subscription(subscription_id)

        if not subscription:
            print(
                f"Subscription not found for invoice: {invoice['id']}, subscription_id: {subscription_id}"
            )
            return

        if not subscription.is_active:
            return

        user = UserService.load_user(subscription.user_id)
        if not user:
            print(f"User not found for subscription: {subscription.id}")
            return

        plan = SubscriptionPlanService.load_plan(subscription.plan_id)
        if not plan:
            print(
                f"Plan not found for subscription: {subscription.id}, plan_id: {subscription.plan_id}"
            )
            return

        # add user credits based on plan amount
        if plan.price > 0:
            UserCreditService.add_subscription_credits(user, plan.name, plan.price)

        print(f"Payment succeeded for invoice: {invoice['id']}, {payload}")
        SubscriptionService.active_subscription(user, subscription.id)

    @staticmethod
    @transaction
    def handle_subscription_canceled(subscription, payload):
        print(f"Subscription canceled: {subscription.id}, {payload}")
        # 在这里更新数据库（例如将用户标记为已取消）
        # Get user from subscription metadata
        user_id = int(subscription["metadata"]["user_id"])
        user = UserService.load_user(user_id)
        if not user:
            return

        # Update user subscription status to inactive
        UserService.update_user_subscription_status(user, "inactive")

    pass
