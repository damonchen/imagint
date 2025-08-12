from typing import Optional
from werkzeug.exceptions import HTTPException


class BaseHTTPException(HTTPException):
    error_code: str = "unknown"
    data: Optional[dict] = None

    def __init__(self, description=None, response=None):
        super(BaseHTTPException, self).__init__(description, response)

        self.data = {
            "code": self.error_code,
            "message": self.description,
            "status": self.code,
        }


class PrivKeyNotFoundError(Exception):
    pass


class UserLoginError(Exception):
    pass


class NotFoundError(Exception):
    pass


class PermissionError(Exception):
    pass


class CaptchaError(Exception):
    pass
