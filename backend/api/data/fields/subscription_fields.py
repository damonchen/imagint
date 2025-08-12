from flask_restful import fields
from ...libs.helper import TimestampField

plan_fields = {
    "id": fields.String(attribute="id"),
    "name": fields.String(attribute="name"),

    "monthly_fee": fields.String(attribute="monthly_fee"),
    "included_tokens": fields.String(attribute="included_tokens"),
    "included_requests": fields.String(attribute="included_requests"),
    "concurrency_limit": fields.String(attribute="concurrency_limit"),
    "extra_token_price": fields.String(attribute="extra_token_price"),
    "extra_request_price": fields.String(attribute="extra_request_price"),
    "feature": fields.String(attribute="feature"),

    "created_by": fields.Integer(attribute="created_by"),
    "created_at": TimestampField(attribute="created_at"),
    "updated_by": fields.Integer(attribute="updated_by"),
    "updated_at": TimestampField(attribute="updated_at"),
}

subscription_fields = {
    "id": fields.String(attribute="id"),
    "user_id": fields.String(attribute="user_id"),
    "plan_id": fields.String(attribute="plan_id"),
    "started_at": fields.String(attribute="started_at"),
    "ended_at": fields.String(attribute="ended_at"),
    "status": fields.String(attribute="status"),
    "auto_renew": fields.String(attribute="auto_renew"),
    "created_by": fields.Integer(attribute="created_by"),
    "created_at": TimestampField(attribute="created_at"),
    "updated_by": fields.Integer(attribute="updated_by"),
    "updated_at": TimestampField(attribute="updated_at"),
}

order_fields = {
    "id": fields.String(attribute="id"),
    "user_id": fields.String(attribute="user_id"),
    "subscription_id": fields.String(attribute="subscription_id"),
    "order_at": fields.String(attribute="order_at"),
    "total_amount": fields.String(attribute="total_amount"),
    "currency": fields.String(attribute="currency"),
    "tax_rate": fields.String(attribute="tax_rate"),
    "status": fields.String(attribute="status"),
    "created_by": fields.Integer(attribute="created_by"),
    "created_at": TimestampField(attribute="created_at"),
    "updated_by": fields.Integer(attribute="updated_by"),
    "updated_at": TimestampField(attribute="updated_at"),
}
