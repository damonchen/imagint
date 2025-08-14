from decimal import Decimal
from api.services.repository.transaction_repository import (
    TransactionRepository,
    UsageRecordRepository,
    RefundRepository,
)

from api.services.subscription_service import OrderService


class UsageRecordService(object):

    @staticmethod
    def create_usage_record(user, tokens_used=0, requests_made=0, cost=Decimal("0.00")):
        usage_record = UsageRecordRepository.create_usage_record(
            user, tokens_used, requests_made, cost
        )

        return usage_record

    @staticmethod
    def list_usage_records(user):
        return UsageRecordRepository.list_usage_records(user)


class RefundService(object):

    @staticmethod
    def create_refund(user, payment_order_id, amount, currency="USD", reason=None):
        order = OrderService.get_order(payment_order_id)
        if order is None:
            return None

        refund = RefundRepository.create_refund(
            user, payment_order_id, order.amount, order.currency, reason
        )

        return refund

    @staticmethod
    def list_refunds(user):
        return RefundRepository.list_refunds(user)

    @staticmethod
    def update_refund_status(user, id, gateway_refund_id, status):
        return RefundRepository.update_refund_status(
            user, id, gateway_refund_id, status
        )

    @staticmethod
    def load_refund(user, id):
        return RefundRepository.list_refund(user, id)


class TransactionService(object):

    @staticmethod
    def load_transaction(user, id):
        return TransactionRepository.load_transaction(user, id)

    @staticmethod
    def list_transactions(user):
        return TransactionRepository.list_transactions(user)

    @staticmethod
    def list_order_transaction(user, order):
        return TransactionRepository.list_order_transaction(user, order)

    @staticmethod
    def create_transaction(
            user,
            order_id,
            type,
            amount,
            currency,
            payment_channel,
            reference_id,
            description=None,
    ):
        order = OrderService.get_order(user, order_id)
        if order is None:
            return None

        return TransactionRepository.create_transaction(
            user,
            order,
            type,
            amount,
            currency,
            payment_channel,
            reference_id,
            description,
        )

    @staticmethod
    def update_transaction_status(user, transaction_id, status):
        return TransactionRepository.update_transaction_status(
            user, transaction_id, status
        )
