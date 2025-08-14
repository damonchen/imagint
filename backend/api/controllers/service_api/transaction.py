from flask_restful import reqparse, marshal_with, Resource
from . import api
from .wraps import WebApiResource
from api.data.fields.transaction_fields import (
    transaction_fields,
    refund_fields,
)
from api.data.fields.subscription_fields import (
    order_fields,
    subscription_fields,
)
from api.libs.decorator import manager_required
from api.services.transaction_service import (
    TransactionService,
    RefundService,
    OrderService,
)
from api.libs.decorator import unified_response
from api.libs.response import make_response


class TransactionCallbackResource(Resource):

    @unified_response(transaction_fields)
    def post(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument("order", type=int, location="json")
        parser.add_argument("type", type=str, location="json")
        parser.add_argument("amount", type=str, location="json")
        parser.add_argument("currency", type=str, location="json")
        parser.add_argument("paymentChannel", type=str, location="json")
        args = parser.parse_args()

        order_id = args.order
        type = args.type
        amount = args.amount
        currency = args.currency
        payment_channel = args.paymentChannel

        transaction = TransactionService.create_transaction(
            user, order_id, type, amount, currency, payment_channel
        )
        return make_response(transaction)


class TransactionsResource(WebApiResource):

    @unified_response(transaction_fields)
    def get(self, user):
        # parser = reqparse.RequestParser()
        # parser.add_argument("type", type=str, location="json")
        # args = parser.parse_args()

        transactions = TransactionService.list_transactions(user)
        return make_response(transactions)


class TransactionResource(WebApiResource):

    @unified_response(transaction_fields)
    def get(self, user, transaction_id):
        transaction = TransactionService.load_transaction(user, transaction_id)
        return make_response(transaction)


class RefundsResource(WebApiResource):

    @unified_response(refund_fields)
    def post(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "payment_order_id", type=int, required=True, location="json"
        )
        parser.add_argument("reason", type=str, location="json")
        args = parser.parse_args()

        payment_order_id = args.payment_order_id
        reason = args.reason

        refund = RefundService.create_refund(user, payment_order_id, reason=reason)

        return make_response(refund)


class RefundResource(WebApiResource):

    @unified_response(refund_fields)
    def get(self, user, refund_id):
        refund = RefundService.load_refund(user, refund_id)
        return make_response(refund)


class RefundStatusResource(WebApiResource):

    @unified_response(refund_fields)
    def post(self, user, refund_id):
        parser = reqparse.RequestParser()
        parser.add_argument("status", type=str, required=True, location="json")
        args = parser.parse_args()

        status = args.status

        refund = RefundService.update_refund_status(user, refund_id, status)
        return make_response(refund)


api.add_resource(TransactionsResource, "/transactions")
api.add_resource(TransactionCallbackResource, "/transactions/callback")
api.add_resource(TransactionResource, "/transactions/<transaction_id>")
api.add_resource(RefundsResource, "/refunds")
api.add_resource(RefundResource, "/refunds/<refund_id>")
api.add_resource(RefundStatusResource, "/refunds/<refund_id>/status")
