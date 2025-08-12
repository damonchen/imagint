from api.extensions.database import db
from api.data.models.transaction import Transaction, Invoice, Refund, UsageRecord
from sqlalchemy import func
from decimal import Decimal
import logging


class InvoiceRepository(object):

    @staticmethod
    def list_invoices(user):
        return db.session.query(Invoice).filter(Invoice.user_id == user.id).all()

    @staticmethod
    def create_invoice(user, period_start, period_end, amount_due, payment_due_date):
        invoice = Invoice(
            user_id=user.id,
            period_start=period_start,
            period_end=period_end,
            amount_due=amount_due,
            amount_paid=Decimal("0.00"),
            payment_due_date=payment_due_date,
        )
        db.session.add(invoice)
        db.session.flush()
        return invoice


class UsageRecordRepository(object):

    @staticmethod
    def list_usage_records(user):
        return (
            db.session.query(UsageRecord).filter(UsageRecord.user_id == user.id).all()
        )

    @staticmethod
    def create_usage_record(user, tokens_used, requests_made, cost):
        record = UsageRecord(
            user_id=user.id,
            tokens_used=tokens_used,
            requests_made=requests_made,
            cost=cost,
        )
        db.session.add(record)
        db.session.flush()

        return record


class RefundRepository(object):

    @staticmethod
    def load_refund(user, id):
        return db.session.query(Refund).filter(Refund.user_id == user.id).get(id)

    @staticmethod
    def list_refunds(user):
        return db.session.query(Refund).filter(Refund.user_id == user.id).all()

    @staticmethod
    def create_refund(user, payment_order_id, amount, currency, reason=None):
        refund = Refund(
            user_id=user.id,
            payment_order_id=payment_order_id,
            amount=amount,
            currency=currency,
            reason=reason,
        )

        db.session.add(refund)
        db.session.flush()

        return refund

    @staticmethod
    def update_refund_status(user, id, gateway_refund_id, status):
        refund = db.session.query(Refund).filter(Refund.user_id == user.id).get(id)
        if refund is None:
            return None

        refund.gateway_refund_id = gateway_refund_id
        refund.status = status

        db.session.add(refund)
        db.session.flush()

        return refund


class TransactionRepository(object):

    @staticmethod
    def load_transaction(user, id):
        return (
            db.session.query(Transaction)
            .filter(Transaction.user_id == user.id)
            .filter(Transaction.id == id)
            .first()
        )

    @staticmethod
    def list_transactions(user):
        return (
            db.session.query(Transaction).filter(Transaction.user_id == user.id).all()
        )

    @staticmethod
    def list_order_transaction(user, order):
        return (
            db.session.query(Transaction)
            .filter(Transaction.user_id == user.id)
            .filter(Transaction.order_id == order.id)
            .all()
        )

    @staticmethod
    def create_transaction(
            user,
            order,
            type,
            amount,
            currency,
            payment_channel,
            reference_id,
            description=None,
    ):
        transaction = Transaction(
            user_id=user.id,
            order_id=order.id,
            type=type,
            amount=amount,
            currency=currency,
            payment_channel=payment_channel,
            reference_id=reference_id,
            description=description,
        )

        db.session.add(transaction)
        db.session.flush()

        return transaction

    @staticmethod
    def update_transaction_status(user, transaction_id, status):
        transaction = (
            db.session.query(Transaction)
            .filter(Transaction.user_id == user.id)
            .get(transaction_id)
        )
        transaction.status = status

        db.session.add(transaction)
        db.session.flush()

        return transaction
