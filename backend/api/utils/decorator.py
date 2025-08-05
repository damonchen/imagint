import json
from functools import wraps
from flask import Response, current_app, request, make_response
from api.libs.helper import get_remote_ip


def api_json(status=200, content_type="application/json;charset=utf-8"):
    def wrap_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resp = func(*args, **kwargs)
            if isinstance(resp, dict):
                resp = Response(
                    json.dumps(resp),
                    status=status,
                    content_type=content_type,
                )

            return resp

        return wrapper

    return wrap_func


def debug_allowed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if not allowed ip, it should response 404
        allowed_debug_ip = current_app.config.get("DEBUG_ALLOWED_IP")
        print("allowed debug ip", allowed_debug_ip)
        if allowed_debug_ip:
            ip = get_remote_ip(request)
            if ip not in allowed_debug_ip:
                return make_response("not founded", 404)
            return func(*args, **kwargs)
        else:
            return make_response("not founded", 404)

    return wrapper
