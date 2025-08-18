import logging
from flask_restful import marshal_with, reqparse
from api.services.credit_service import UserCreditService
from api.data.fields.credit_fields import (
    credit_info_fields,
    subscription_plans_fields,
    credit_transactions_fields,
)
from . import api
from .wraps import WebApiResource
from api.libs.decorator import unified_response
from api.libs.response import make_response

logger = logging.getLogger(__name__)


class UserCreditResource(WebApiResource):
    """用户Credit信息API"""

    @unified_response(credit_info_fields)
    def get(self, user):
        """获取用户credit信息"""
        credit_info = UserCreditService.get_user_credit_info(user)
        logger.info("get credit info feilds %s", credit_info)
        return make_response(credit_info)


class SubscriptionPlansResource(WebApiResource):
    """订阅计划API"""

    @unified_response(subscription_plans_fields)
    def get(self, user):
        """获取可用的订阅计划"""
        plans = UserCreditService.get_subscription_plans()
        return make_response({"plans": plans})


class CreditTransactionResource(WebApiResource):
    """Credit交易记录API"""

    @unified_response(credit_transactions_fields)
    def get(self, user):
        """获取用户credit交易记录"""
        parser = reqparse.RequestParser()
        parser.add_argument("page", type=int, default=1, location="args")
        parser.add_argument("per_page", type=int, default=20, location="args")
        args = parser.parse_args()

        transactions_pagination = UserCreditService.get_user_transactions_pagination(
            user_id=user.id, page=args.page, per_page=args.per_page
        )

        logger.info("transaction pagination info is %s, %s", transactions_pagination.items, dir(transactions_pagination))

        return make_response({
            "transactions": transactions_pagination.items,
            "total": transactions_pagination.total,
            "page": transactions_pagination.page,
            "page_size": transactions_pagination.per_page
        })


# API路由
api.add_resource(UserCreditResource, "/user/credits")
api.add_resource(SubscriptionPlansResource, "/subscription/plans")
api.add_resource(CreditTransactionResource, "/user/credits/transactions")
