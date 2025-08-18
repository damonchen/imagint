from flask_restful import fields
from ...libs.helper import TimestampField

plan_fields = {
    "id": fields.String(attribute="id"),
    "name": fields.String(attribute="name"),
    "description": fields.String(attribute="description"),
    "interval": fields.String(attribute="interval"),
    "intervalCount": fields.String(attribute="interval_count"),
    "price": fields.String(attribute="price"),
    "creditAmount": fields.String(attribute="credit_amount"),
    "isActive": fields.String(attribute="is_active"),
    "createdBy": fields.String(attribute="created_by"),
    "createdAt": TimestampField(attribute="created_at"),
    "updatedBy": fields.String(attribute="updated_by"),
    "updatedAt": TimestampField(attribute="updated_at"),
}

list_plan_fields = fields.List(fields.Nested(plan_fields))

order_fields = {
    "id": fields.String(attribute="id"),
    "subscriptionId": fields.String(attribute="subscription_id"),
    "amount": fields.String(attribute="amount"),
    "discountAmount": fields.String(attribute="discount_amount"),
    "paid_amount": fields.String(attribute="paid_amount"),
    "paymentChannel": fields.String(attribute="payment_channel"),
    "status": fields.String(attribute="status"),
    "createdBy": fields.String(attribute="created_by"),
    "created_at": TimestampField(attribute="created_at"),
    "updated_by": fields.String(attribute="updated_by"),
    "updated_at": TimestampField(attribute="updated_at"),
}

list_order_fields = fields.List(fields.Nested(order_fields))
