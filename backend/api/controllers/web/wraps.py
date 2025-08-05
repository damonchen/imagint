import logging
from functools import wraps

from flask import request, g, make_response, session, redirect
from flask_restful import Resource
from werkzeug.exceptions import NotFound, Unauthorized
from api.extensions.login import token_coder
from api.extensions.database import db
from api.data.models.account import Account


def validate_api_token(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        account = decode_jwt_token()
        return func(account, *args, **kwargs)

    return wrapper


def decode_jwt_token():
    auth_header = request.headers.get("Authorization")
    if auth_header is None or " " not in auth_header:
        raise Unauthorized(
            "Authorization header must be provided and start with 'Bearer'"
        )

    auth_scheme, auth_token = auth_header.split(None, 1)
    if auth_scheme.lower() != "bearer":
        raise Unauthorized("Invalid authorization scheme")

    payload = token_coder.decode(auth_token)
    account_id = payload["account_id"]

    account = db.session.query(Account).filter(Account.id == account_id).first()
    if account is None:
        raise NotFound()

    g.account = account
    return account


class WebApiResource(Resource):
    method_decorators = [validate_api_token]
