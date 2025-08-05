import logging
from functools import wraps
from flask import g, make_response, request, session, redirect
from api.services.account_service import AccountService
from api.extensions.login import token_coder

logger = logging.getLogger("decorator")


def manager_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        account = g.account
        if not account.is_manager:
            logger.error(f"account {account.email} is not manager")
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
                account_id = payload["account_id"]

                account = AccountService.load_account(account_id)
                if account is None:
                    return make_response("Forbidden", 403)

                g.account = account
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
        account = g.account
        if account is None:
            logger.error("account not exist")
            return make_response("Forbidden", 403)

        if (
                account.has_finance_manager
                or account.has_cashier
                or account.hash_accountant
        ):
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
