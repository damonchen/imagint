import logging
from flask_restful import marshal_with, reqparse
from api.libs.decorator import manager_required
from api.data.fields.account_fields import (
    list_account_fields,
    account_partial_fields,
)
from api.services.account_service import AccountService

from . import api
from .wraps import WebApiResource


class AccountsResource(WebApiResource):
    # 越是基础的，越需要放到最后面，这个是实现依赖

    @manager_required
    @marshal_with(list_account_fields)
    def get(self, account):
        accounts = AccountService.load_accounts()
        return accounts


class AccountResource(WebApiResource):

    @manager_required
    @marshal_with(account_partial_fields)
    def get(self, account, pk):
        account = AccountService.load_account(pk)
        return account


class AccountSelfResource(WebApiResource):

    @marshal_with(account_partial_fields)
    def get(self, account):
        return account

    @marshal_with(account_partial_fields)
    def put(self, account):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, location="json")
        parser.add_argument("password", type=str, location="json")
        args = parser.parse_args()

        username = args.username
        password = args.password

        return AccountService.change_password(
            account,
            username=username,
            password=password,
        )


api.add_resource(AccountSelfResource, "/self")

api.add_resource(AccountsResource, "/accounts")
api.add_resource(AccountResource, "/accounts/<pk>")
