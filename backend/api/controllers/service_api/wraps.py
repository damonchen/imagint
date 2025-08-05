import logging
from collections.abc import Callable
from typing import Optional
from enum import Enum
from functools import wraps

from pydantic import BaseModel
from flask import g, request, make_response, session, redirect
from werkzeug.exceptions import Unauthorized

from api.extensions.database import db
from api.data.models.model import ApiToken


class UserLocation(Enum):
    QUERY = "query"
    JSON = "json"
    FORM = "form"


class FetchUser(BaseModel):
    fetch_from: UserLocation
    required: bool = False


def validate_app_token(
    view: Optional[Callable] = None, *, fetch_user: Optional[FetchUser] = None
):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            api_token = validate_and_get_api_token("app")
            kwargs["api_token"] = api_token

            if fetch_user_args := fetch_user:
                if fetch_user_args.required:
                    if fetch_user_args.fetch_from == UserLocation.QUERY:
                        user_id = request.args.get("user")
                    elif fetch_user_args.fetch_from == UserLocation.JSON:
                        user_id = request.get_json().get("user")
                    elif fetch_user_args.fetch_from == UserLocation.FORM:
                        user_id = request.form.get("user")
                    else:
                        user_id = None

                    if not user_id and fetch_user_args.required:
                        raise ValueError("user id is required")

                    kwargs["user_id"] = user_id

            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator


def validate_and_get_api_token(scope=None):
    auth_header = request.headers.get("Authorization")
    if auth_header is None or " " not in auth_header:
        raise Unauthorized(
            "Authorization header must be provided and start with 'Bearer'"
        )

    auth_scheme, auth_token = auth_header.split(None, 1)
    if auth_scheme.lower() != "bearer":
        raise Unauthorized("Invalid authorization scheme")

    api_token = (
        db.session.query(ApiToken)
        .filter(
            ApiToken.token == auth_token,
            ApiToken.type == scope,
        )
        .first()
    )
    if api_token is None:
        raise Unauthorized("Invalid token")

    return api_token
