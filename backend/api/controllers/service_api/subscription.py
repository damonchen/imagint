import logging
from flask_restful import Resource, marshal_with, reqparse

from api.extensions.database import db
from api.libs.decorator import manager_required

from api.data.models.subscription import Plan
from api.services.subscription_service import OrderService, SubscriptionService
from api.data.fields.plan_fields import (
    plan_fields,
    subscription_fields,
    order_fields,
    list_subscription_fields,
)

from . import api
from .wraps import WebApiResource


class PlanApiResource(Resource):

    @marshal_with(plan_fields)
    def get(self):
        return db.session.query(Plan).all()


class PlanPayResource(WebApiResource):

    @marshal_with(subscription_fields)
    def post(self, user, plan_id):
        subscription = SubscriptionService.create_subscription(user, plan_id)
        return subscription


class SubscriptionsResource(WebApiResource):

    @marshal_with(list_subscription_fields)
    def get(self, user):
        return SubscriptionService.list_subscriptions(user)


class SubscriptionResource(WebApiResource):

    @marshal_with(subscription_fields)
    def get(self, user, subscription_id):
        subscription = SubscriptionService.load_subscription(subscription_id)
        return subscription


class SubscriptionPaymentResource(WebApiResource):

    @marshal_with(order_fields)
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

        return order


class OrderCancelResource(WebApiResource):

    @manager_required
    @marshal_with(order_fields)
    def put(self, user, order_id):
        order = OrderService.cancel_order(user, order_id)
        return order


class OrderRefundResource(WebApiResource):

    @manager_required
    @marshal_with(order_fields)
    def put(self, user, order_id):
        order = OrderService.refund_order(user, order_id)
        return order


class OrderSuccessResource(WebApiResource):

    @manager_required
    @marshal_with(order_fields)
    def put(self, user, order_id):
        order = OrderService.success_order(user, order_id)
        return order


class OrderFailResource(WebApiResource):

    @manager_required
    @marshal_with(order_fields)
    def put(self, user, order_id):
        order = OrderService.fail_order(user, order_id)
        return order


class OrderStartResource(WebApiResource):

    @manager_required
    @marshal_with(order_fields)
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
        return order


class OrdersResource(WebApiResource):

    @marshal_with(order_fields)
    def get(self, user):
        return OrderService.list_orders(user)


class OrderResource(WebApiResource):

    @marshal_with(order_fields)
    def get(self, user, order_id):
        order = OrderService.get_order(user, order_id)
        return order


api.add_resource(PlanApiResource, "/plans")
api.add_resource(PlanPayResource, "/plans/<plan_id>/pay")

api.add_resource(SubscriptionsResource, "/subscriptions")
api.add_resource(SubscriptionResource, "/subscriptions/<subscription_id>")
api.add_resource(SubscriptionPaymentResource, "/subscriptions/<subscription_id>/pay")

api.add_resource(OrdersResource, "/orders")
api.add_resource(OrderResource, "/orders/<order_id>")
api.add_resource(OrderCancelResource, "/order/<order_id>/cancel")
api.add_resource(OrderRefundResource, "/order/<order_id>/refund")
api.add_resource(OrderSuccessResource, "/order/<order_id>/success")
api.add_resource(OrderFailResource, "/order/<order_id>/fail")
api.add_resource(OrderStartResource, "/order/<order_id>/start")
