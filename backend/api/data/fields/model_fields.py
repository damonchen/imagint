from flask_restful import fields
from ...libs.helper import TimestampField

setup_fields = {
    "id": fields.String(attribute="id"),
    "version": fields.String(attribute="version"),
    "setupAt": fields.DateTime(attribute="setup_at"),
}


api_token_fields = {
    "id": fields.String(attribute="id"),
    "appId": fields.String(attribute="app_id"),
    "type": fields.String(attribute="type"),
    "token": fields.String(attribute="token"),
    # createdBy": fields.String(attribute='created_by'),
    "createdAt": TimestampField(attribute="created_at"),
    # updatedBy": fields.String(attribute='updated_by'),
    "updatedAt": TimestampField(attribute="updated_at"),
}
