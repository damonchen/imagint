import logging
from flask_restful import Resource

from .wraps import WebApiResource
from api.libs.decorator import manager_required
from api.services.audit_service import AuditService

from . import api


class SetupResource(Resource):
    @manager_required
    def get(self):
        return AuditService.app_setup()


class OperationResource(WebApiResource):

    @manager_required
    def get(self, account):
        return AuditService.list_operations_by_account(account_id=account.id)


api.add_resource(
    SetupResource,
    "/setup",
)
api.add_resource(
    OperationResource,
    "/operation",
)
