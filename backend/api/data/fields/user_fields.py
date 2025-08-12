from flask_restful import fields
from ...libs.helper import TimestampField

user_fields = {
    "id": fields.Integer,
    "email": fields.String(),
    "google_user_id": fields.String(),
    "username": fields.String,
    "avatar": fields.String(),
    "status": fields.String,
    "option": fields.Raw(),
    "language": fields.String,
    "theme": fields.String,
    "timezone": fields.String,
    "invited_by": fields.Integer(),
    "last_login_at": TimestampField(),
    "created_at": TimestampField,
    "updated_at": TimestampField,
}

user_partial_fields = {
    "id": fields.Integer,
    "email": fields.String(),
    "username": fields.String,
    "avatar": fields.String(),
    "status": fields.String,
}

user_pagination_fields = {
    "page": fields.Integer,
    "limit": fields.Integer(attribute="per_page"),
    "total": fields.Integer,
    "hasMore": fields.Boolean(attribute="has_next"),
    "data": fields.List(fields.Nested(user_partial_fields), attribute="items"),
}

list_user_fields = fields.List(fields.Nested(user_partial_fields))

user_password_reset_token_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "token": fields.String,
    "expires_at": TimestampField,
}

google_user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "username": fields.String(),
    "avatar": fields.String(),
    "google_user_id": fields.String,
    "created_by": fields.Integer,
    "created_at": TimestampField,
    "updated_by": fields.Integer,
    "updated_at": TimestampField,
}
