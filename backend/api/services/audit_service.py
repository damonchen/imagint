import logging
from flask import request
from api.extensions.database import db
from api.data.models.model import AppSetup, OperationLog
from api.libs.helper import get_remote_ip


class AuditService(object):

    @staticmethod
    def app_setup():
        return db.session.query(AppSetup).all()

    @staticmethod
    def add_operation(user_id, action, payload, created_by):
        ip = get_remote_ip(request)
        operation = OperationLog(
            user_id=user_id,
            action=action,
            payload=payload,
            created_by=created_by,
            ip=ip,
        )
        db.session.add(operation)
        db.session.flush()

        return operation

    @staticmethod
    def list_operations():
        return db.session.query(OperationLog).all()

    @staticmethod
    def list_operations_by_user(user_id):
        return (
            db.session.query(OperationLog).filter(OperationLog.user_id == user_id).all()
        )
