import logging
from functools import wraps

from flask import request, g, make_response, session, redirect
from flask_restful import Resource
from werkzeug.exceptions import NotFound, Unauthorized
from api.extensions.login import token_coder
from api.extensions.database import db
from api.data.models.account import Account
from api.services.task_service import TaskWorkerService


def validate_api_token(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        account = decode_jwt_token()
        return func(account, *args, **kwargs)

    return wrapper


def validate_task_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        task_web_token = decode_task_token()
        g.task_web_token = task_web_token

        return func(*args, **kwargs)

    return wrapper


def decode_task_token():
    api_key = request.headers.get("X-API-KEY")
    if api_key is None:
        raise Unauthorized("X-API-KEY header must be provided")

    task_web_token = TaskWorkerService.get_task_token(api_key)
    if task_web_token is None:
        raise Unauthorized("Invalid API key")

    if task_web_token.is_not_active:
        raise Unauthorized("Invalid API key")

    return task_web_token


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


class TaskApiResource(Resource):
    method_decorators = [validate_task_token]
