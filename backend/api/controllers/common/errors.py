from api.libs.exceptions import BaseHTTPException


class NotFoundError(BaseHTTPException):
    error_code = "not_found"
    description = "Resource not found."
    code = 400


class CreatedUserError(BaseHTTPException):

    error_code = "created_user_error"
    description = "created user error"
    code = 400


class PermissionError(BaseHTTPException):
    error_code = "permission_error"
    description = "Permission denied."
    code = 403


class NotWorkflowAppError(BaseHTTPException):
    error_code = "not_workflow_app"
    description = "Please check if your Workflow app mode matches the right API route."
    code = 400


class NoContainerError(BaseHTTPException):
    error_code = "no_container"
    description = "Container Id or Container Type not found."
    code = 400


class NoFileUploadedError(BaseHTTPException):
    error_code = "no_file_uploaded"
    description = "Should upload your file."
    code = 400


class TooManayFilesError(BaseHTTPException):
    error_code = "too_many_files"
    description = "Only one file is allowed."
    code = 400


class FileTooLargeError(BaseHTTPException):
    error_code = "file_too_large"
    description = "File size exceeded the limit. {message}"
    code = 413


class UnsupportedFileTypeError(BaseHTTPException):
    error_code = "unsupported_file_type"
    description = "File type not allowed."
    code = 415


class TimeRangeError(BaseHTTPException):
    error_code = "time_range_error"
    description = "Time range error"
    code = 400


class NoInvitedCodeError(BaseHTTPException):
    error_code = "no_invited_code"
    description = "invited code not exist"
    code = 400


class AuthenticationError(BaseHTTPException):
    error_code = "authentication_error"
    description = "user not exists or password not valid"
    code = 400


class InvalidCodeError(BaseHTTPException):
    error_code = "invalid_code"
    description = "authorized code not valid"
    code = 400
