from flask_restful import fields

usage_record_fields = {
    "id": fields.String(attribute="id"),
    "userId": fields.String(attribute="user_id"),
    "usageAt": fields.String(attribute="usage_at"),
    "tokensUsed": fields.Integer(attribute="tokens_used"),
    "requestsMade": fields.Integer(attribute="requests_made"),
    "cost": fields.String(attribute="cost"),
    "updatedAt": fields.String(attribute="updated_at"),
    "createdAt": fields.String(attribute="created_at"),
}

refund_fields = {
    "id": fields.String(attribute="id"),
    "userId": fields.String(attribute="user_id"),
    "paymentOrderId": fields.String(attribute="payment_order_id"),
    "amount": fields.String(attribute="amount"),
    "currency": fields.String(attribute="currency"),
    "status": fields.String(attribute="status"),
    "gatewayRefundId": fields.String(attribute="gateway_refund_id"),
    "reason": fields.String(attribute="reason"),
    "updatedAt": fields.String(attribute="updated_at"),
    "createdAt": fields.String(attribute="created_at"),
}

transaction_fields = {
    "id": fields.String(attribute="id"),
    "userId": fields.String(attribute="user_id"),
    "orderId": fields.String(attribute="order_id"),
    "type": fields.String(attribute="type"),
    "amount": fields.String(attribute="amount"),
    "currency": fields.String(attribute="currency"),
    "status": fields.String(attribute="status"),
    "amount": fields.String(attribute="amount"),
    "paymentChannel": fields.String(attribute="payment_channel"),
    "referenceId": fields.String(attribute="reference_id"),
    "description": fields.String(attribute="description"),
    "updatedAt": fields.String(attribute="updated_at"),
    "createdAt": fields.String(attribute="created_at"),
}
