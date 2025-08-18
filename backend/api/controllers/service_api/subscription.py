import json
import logging

from flask import jsonify, current_app
from flask_restful import Resource, marshal_with, reqparse

from api.extensions.database import db
from api.libs.decorator import manager_required

from api.data.models.subscription import SubscriptionPlan
from api.services.subscription_service import (
    OrderService,
    SubscriptionService,
    SubscriptionPlanService,
)
from api.data.fields.plan_fields import (
    plan_fields,
    order_fields,
)
from api.data.fields.subscription_fields import (
    subscription_fields,
    list_subscription_fields,
    subscription_url_fields,
    cancel_subscription_fields,
)

from api.extensions.stripe import stripe
from api.services.redis_service import RedisService

from . import api
from .wraps import WebApiResource
from api.libs.decorator import unified_response
from api.libs.response import make_response
from ...data.models.enums import PaymentChannelStatus

logger = logging.getLogger(__name__)


class PlanApiResource(Resource):

    @unified_response(plan_fields)
    def get(self):
        plans = SubscriptionPlanService.load_plans()
        return make_response(plans)


class SubscriptionsResource(WebApiResource):

    @unified_response(subscription_fields)
    def get(self, user):
        subscriptions = SubscriptionService.list_subscriptions(user)
        return make_response(subscriptions)

    @unified_response(subscription_url_fields)
    def post(self, user):
        # 构建订阅
        parser = reqparse.RequestParser()
        parser.add_argument("plan", type=str, location="json")

        args = parser.parse_args()
        email = user.email
        plan = args.plan

        app_web_url = current_app.config["APP_WEB_URL"]
        flag, info = SubscriptionService.start_subscription(user, email, plan, app_web_url)
        if not flag:
            return make_response(status="fail", message=info)

        return make_response({"sessionId": info.id, "checkoutUrl": info.url})


class SubscriptionResource(WebApiResource):

    @unified_response(subscription_fields)
    def get(self, user, subscription_id):
        subscription = SubscriptionService.load_subscription(subscription_id)
        return make_response(subscription)


class SubscriptionCancelResource(WebApiResource):

    @unified_response(subscription_fields)
    def post(self, user, subscription_id):
        subscription = SubscriptionService.cancel_subscription(user, subscription_id)
        logger.info("subscription cancel data %s", subscription)
        return subscription


class SubscriptionPaymentResource(WebApiResource):

    @unified_response(order_fields)
    def post(self, user, subscription_id):
        parser = reqparse.RequestParser()
        parser.add_argument("channel", type=str, location="json")
        parser.add_argument("plan", type=str, location="json")

        args = parser.parse_args()

        channel = args.channel

        order = OrderService.create_order(
            user,
            subscription_id,
            channel,
        )

        return make_response(order)


class OrderCancelResource(WebApiResource):

    @manager_required
    @unified_response(order_fields)
    def put(self, user, order_id):
        order = OrderService.cancel_order(user, order_id)
        return make_response(order)


class OrderRefundResource(WebApiResource):

    @manager_required
    @unified_response(order_fields)
    def put(self, user, order_id):
        order = OrderService.refund_order(user, order_id)
        return make_response(order)


class OrderSuccessResource(WebApiResource):

    @manager_required
    @unified_response(order_fields)
    def put(self, user, order_id):
        order = OrderService.success_order(user, order_id)
        return make_response(order)


class OrderFailResource(WebApiResource):

    @manager_required
    @unified_response(order_fields)
    def put(self, user, order_id):
        order = OrderService.fail_order(user, order_id)
        return make_response(order)


class OrderStartResource(WebApiResource):

    @manager_required
    @unified_response(order_fields)
    def put(self, user, order_id):
        parser = reqparse.RequestParser()
        parser.add_argument("channel", type=str, location="json")
        args = parser.parse_args()

        channel = args.channel

        order = OrderService.start_order(
            user,
            order_id,
            channel,
        )
        return make_response(order)


class OrdersResource(WebApiResource):

    @unified_response(order_fields)
    def get(self, user):
        orders = OrderService.list_orders(user)
        return make_response(orders)


class OrderResource(WebApiResource):

    @unified_response(order_fields)
    def get(self, user, order_id):
        order = OrderService.get_order(user, order_id)
        return make_response(order)


api.add_resource(PlanApiResource, "/plans")

api.add_resource(SubscriptionsResource, "/subscriptions")
api.add_resource(SubscriptionResource, "/subscriptions/<subscription_id>")
# api.add_resource(SubscriptionCancelResource, "/subscriptions/<subscription_id>/cancel")
api.add_resource(SubscriptionPaymentResource, "/subscriptions/<subscription_id>/pay")
api.add_resource(SubscriptionCancelResource, "/subscriptions/<subscription_id>/cancel")

api.add_resource(OrdersResource, "/orders")
api.add_resource(OrderResource, "/orders/<order_id>")
api.add_resource(OrderCancelResource, "/order/<order_id>/cancel")
api.add_resource(OrderRefundResource, "/order/<order_id>/refund")
api.add_resource(OrderSuccessResource, "/order/<order_id>/success")
api.add_resource(OrderFailResource, "/order/<order_id>/fail")
api.add_resource(OrderStartResource, "/order/<order_id>/start")
