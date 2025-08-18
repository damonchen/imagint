from flask_restful import fields
from ...libs.helper import TimestampField

plan_fields = {
    "id": fields.String(attribute="id"),
    "name": fields.String(attribute="name"),
    "monthlyFee": fields.String(attribute="monthly_fee"),
    "includedTokens": fields.String(attribute="included_tokens"),
    "includedRequests": fields.String(attribute="included_requests"),
    "concurrencyLimit": fields.String(attribute="concurrency_limit"),
    "extraTokenPrice": fields.String(attribute="extra_token_price"),
    "extraRequestPrice": fields.String(attribute="extra_request_price"),
    "feature": fields.String(attribute="feature"),
    "createdBy": fields.Integer(attribute="created_by"),
    "createdAt": TimestampField(attribute="created_at"),
    "updatedBy": fields.Integer(attribute="updated_by"),
    "updatedAt": TimestampField(attribute="updated_at"),
}

subscription_url_fields = {
    "sessionId": fields.String(),
    "checkoutUrl": fields.String(),
}

cancel_subscription_fields = {
    "id": fields.String(attribute="id"),
    "status": fields.String(attribute="status"),
    "canceledAt": fields.String(attribute="canceled_at"),
}

order_fields = {
    "id": fields.String(attribute="id"),
    "userId": fields.String(attribute="user_id"),
    "subscriptionId": fields.String(attribute="subscription_id"),
    "orderAt": fields.String(attribute="order_at"),
    "totalAmount": fields.String(attribute="total_amount"),
    "currency": fields.String(attribute="currency"),
    "taxRate": fields.String(attribute="tax_rate"),
    "status": fields.String(attribute="status"),
    "createdBy": fields.Integer(attribute="created_by"),
    "createdAt": TimestampField(attribute="created_at"),
    "updatedBy": fields.Integer(attribute="updated_by"),
    "updatedAt": TimestampField(attribute="updated_at"),
}

subscription_fields = {
    "id": fields.String(attribute="id"),
    "userId": fields.String(attribute="user_id"),
    "planId": fields.String(attribute="plan_id"),
    "startedAt": fields.String(attribute="started_at"),
    "endedAt": fields.String(attribute="ended_at"),
    "status": fields.String(attribute="status"),
    "autoRenew": fields.String(attribute="auto_renew"),
    "createdBy": fields.String(attribute="created_by"),
    "createdAt": TimestampField(attribute="created_at"),
    "updatedBy": fields.String(attribute="updated_by"),
    "updatedAt": TimestampField(attribute="updated_at"),
}

list_subscription_fields = fields.List(fields.Nested(subscription_fields))
