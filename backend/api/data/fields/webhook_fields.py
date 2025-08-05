from flask_restful import fields
from ...libs.helper import TimestampField

wehook_fields = {
    "id": fields.String(attribute="id"),
    "userId": fields.String(attribute="user_id"),
    "event": fields.String(attribute="event"),
    # "createdBy": fields.String(attribute='created_by'),
    "createdAt": TimestampField(attribute="created_at"),
    # "updatedBy": fields.String(attribute='updated_by'),
    "updatedAt": TimestampField(attribute="updated_at"),
}


webhook_list_fields = {"webhooks": fields.List(fields.Nested(wehook_fields))}

webhook_record_fields = {
    "id": fields.String(attribute="id"),
    "webhookId": fields.String(attribute="webhook_id"),
    "userId": fields.String(attribute="user_id"),
    "event": fields.String(attribute="event"),
    "payload": fields.String(attribute="payload"),
    # "createdBy": fields.String(attribute='created_by'),
    "createdAt": TimestampField(attribute="created_at"),
    # "updatedBy": fields.String(attribute='updated_by'),
    "updatedAt": TimestampField(attribute="updated_at"),
}

webhook_record_list_fields = fields.List(fields.Nested(webhook_record_fields))
