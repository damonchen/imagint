import logging
from functools import wraps
from typing import Union

from flask import g, make_response, request, session, redirect
from flask_restful import fields, marshal
from api.services.user_service import UserService
from api.extensions.login import token_coder

logger = logging.getLogger("decorator")


def manager_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = g.user
        if not user.is_manager:
            logger.error(f"user {user.email} is not manager")
            return make_response("Forbidden", 403)

        return func(*args, **kwargs)

    return wrapper


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            authorization = request.headers["Authorization"]
            scheme, token = authorization.split(" ")
            if scheme == "Bearer":
                payload = token_coder.decode(token)
                user_id = payload["user_id"]

                user = UserService.load_user(user_id)
                if user is None:
                    return make_response("Forbidden", 403)

                g.user = user
            else:
                logger.error("scheme not bearer")
                return make_response("Forbidden", 403)
        else:
            logger.error("request not found Authorization header")
            return make_response("Forbidden", 403)

        return func(*args, **kwargs)

    return wrapper


def any_required(required_funcs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for required_func in required_funcs:
                response = required_func(func)(*args, **kwargs)
                if response.status_code == 200:
                    return response

            logger.info("all required funcs not succeed")
            return make_response("Forbidden", 403)

        return wrapper

    return decorator


def finance_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = g.user
        if user is None:
            logger.error("user not exist")
            return make_response("Forbidden", 403)

        if user.has_finance_manager or user.has_cashier or user.hash_userant:
            return func(*args, **kwargs)
        else:
            return make_response("Forbidden", 403)

    return wrapper


def openid_required(func):
    from .wechat import get_authorize_url

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "openid" not in session:
            return redirect(get_authorize_url())

        return func(*args, **kwargs)

    return wrapper


# 这是所有 API 公用的外层结构
base_response_fields = {
    "status": fields.String,  # ok / limit / error
    "message": fields.String,  # 提示信息
    "data": Union[fields.Raw, fields.Nested],  # 子结构（每个 API 自己定义）
}


def unified_response(data_fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resp = func(*args, **kwargs)
            fields_copy = base_response_fields.copy()
            fields_copy["data"] = fields.Nested(data_fields, allow_null=True)

            # logger.info("fields copy info %s == %s", fields_copy, resp )

            return marshal(resp, fields_copy)

        return wrapper

    return decorator
