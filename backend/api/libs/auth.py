import os
import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional
from functools import wraps
from flask import request, current_app, g, has_request_context
from werkzeug.local import LocalProxy
from werkzeug.exceptions import Unauthorized

from api.extensions.login import login_manager
from .helper import is_valid_authorization

current_user = LocalProxy(lambda: _get_user())


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if auth_header:
            if is_valid_authorization(auth_header):
                raise Unauthorized(
                    'Invalid authorization header. Excpeted "Bearer <token>"'
                )
        auth_scheme, auth_token = auth_header.split(" ", 1)
        auth_scheme = auth_scheme.lower()
        if auth_scheme != "bearer":
            raise Unauthorized(
                'Invalid authorization header. Excpeted "Bearer <token>"'
            )

        # TODO: is valid token

        if not current_user.is_authenticated:
            return login_manager.unauthorized()

        # flask 1.x compatibility
        # current_app.ensure_sync is only available in Flask >= 2.0
        if callable(getattr(current_app, "ensure_sync", None)):
            return current_app.ensure_sync(func)(*args, **kwargs)

        return func(*args, **kwargs)

    return wrapper


def _get_user():
    if has_request_context():
        if hasattr(g, "_current_user"):
            login_manager._load_user()

        return g._current_user

    return None
