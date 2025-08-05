from .base import BaseServiceError


class NotFoundError(BaseServiceError):
    pass


class NotPermittedError(BaseServiceError):
    pass


class ValidationError(BaseServiceError):
    pass
