from flask_restful import fields
from ...libs.helper import TimestampField


credit_info_fields = {
    "balance": fields.Integer(attribute="balance"),
    "dailyCreditsUsed": fields.Integer(attribute="daily_credits_used"),
    "canGenerate": fields.Boolean(attribute="can_generate"),
    "imagesRemaining": fields.Integer(attribute="images_remaining"),
    "lastDailyReset": fields.String(attribute="last_daily_reset"),
}

subscription_plan_fields = {
    "id": fields.Integer(attribute="id"),
    "name": fields.String(attribute="name"),
    "priceUsd": fields.Integer(attribute="price_usd"),
    "priceDisplay": fields.String(attribute="price_display"),
    "creditAmount": fields.Integer(attribute="credit_amount"),
    "durationDays": fields.Integer(attribute="duration_days"),
    "imagesIncluded": fields.Integer(attribute="images_included"),
}

subscription_plans_fields = {
    "plans": fields.List(fields.Nested(subscription_plan_fields))
}

credit_transaction_fields = {
    "id": fields.Integer(attribute="id"),
    "userId": fields.Integer(attribute="user_id"),
    "amount": fields.Integer(attribute="amount"),
    "balanceAfter": fields.Integer(attribute="balance_after"),
    "transactionType": fields.String(attribute="transaction_type"),
    "source": fields.String(attribute="source"),
    "description": fields.String(attribute="description"),
    "createdAt": TimestampField(attribute="created_at"),
}

credit_transactions_fields = {
    "transactions": fields.List(fields.Nested(credit_transaction_fields)),
    "total": fields.Integer(attribute="total"),
    "page": fields.Integer(attribute="page"),
    "pageSize": fields.Integer(attribute="page_size"),
}
