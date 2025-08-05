from flask_restful import fields
from ...libs.helper import TimestampField

plan_fields = {
    "id": fields.String(attribute="id"),
    "name": fields.String(attribute="name"),
    "description": fields.String(attribute="description"),
    "price": fields.String(attribute="price"),
    "discount_amount": fields.String(attribute="discount_amount"),
    "month": fields.String(attribute="month"),
    "created_by": fields.String(attribute="created_by"),
    "created_at": TimestampField(attribute="created_at"),
    "updated_by": fields.String(attribute="updated_by"),
    "updated_at": TimestampField(attribute="updated_at"),
}

list_plan_fields = fields.List(fields.Nested(plan_fields))


subscription_fields = {
    "id": fields.String(attribute="id"),
    "account_id": fields.String(attribute="account_id"),
    "plan_id": fields.String(attribute="plan_id"),
    "started_at": fields.String(attribute="started_at"),
    "ended_at": fields.String(attribute="ended_at"),
    "status": fields.String(attribute="status"),
    "created_by": fields.String(attribute="created_by"),
    "created_at": TimestampField(attribute="created_at"),
    "updated_by": fields.String(attribute="updated_by"),
    "updated_at": TimestampField(attribute="updated_at"),
}

list_subscription_fields = fields.List(fields.Nested(subscription_fields))


order_fields = {
    "id": fields.String(attribute="id"),
    "subscription_id": fields.String(attribute="subscription_id"),
    "amount": fields.String(attribute="amount"),
    "discount_amount": fields.String(attribute="discount_amount"),
    "paid_amount": fields.String(attribute="paid_amount"),
    "payment_channel": fields.String(attribute="payment_channel"),
    "status": fields.String(attribute="status"),
    "created_by": fields.String(attribute="created_by"),
    "created_at": TimestampField(attribute="created_at"),
    "updated_by": fields.String(attribute="updated_by"),
    "updated_at": TimestampField(attribute="updated_at"),
}

list_order_fields = fields.List(fields.Nested(order_fields))
