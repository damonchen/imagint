from flask_restful import fields
from ...libs.helper import TimestampField

user_fields = {
    "id": fields.Integer,
    "email": fields.String(),
    "googleUserId": fields.String(),
    "username": fields.String,
    "avatar": fields.String(),
    "status": fields.String,
    "option": fields.Raw(),
    "language": fields.String,
    "theme": fields.String,
    "timezone": fields.String,
    "invitedBy": fields.Integer(),
    "lastLoginAt": TimestampField(),
    "createdAt": TimestampField,
    "updatedAt": TimestampField,
}

user_partial_fields = {
    "id": fields.Integer,
    "theme": fields.String(),
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
    "userId": fields.Integer,
    "token": fields.String,
    "expiresAt": TimestampField,
}

google_user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "username": fields.String(),
    "avatar": fields.String(),
    "googleUserId": fields.String,
    "createdBy": fields.Integer,
    "createdAt": TimestampField,
    "updatedBy": fields.Integer,
    "updatedAt": TimestampField,
}
