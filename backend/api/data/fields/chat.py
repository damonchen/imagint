from flask_restful import fields
from ...libs.helper import TimestampField


chat_fields = {
    "id": fields.String(attribute="id"),
    "title": fields.String(attribute="title"),
    "createdAt": TimestampField(attribute="created_at"),
}

page_chat_fields = {
    "items": fields.List(fields.Nested(chat_fields)),
    "total": fields.Integer(attribute="total"),
    "page": fields.Integer(attribute="page"),
    "page_size": fields.Integer(attribute="page_size"),
}


chat_message_fields = {
    "id": fields.String(attribute="id"),
    "chat_id": fields.String(attribute="chat_id"),
    "image_path_ids": fields.String(attribute="image_path_ids"),
    "translated_image_path_ids": fields.String(attribute="translated_image_path_ids"),
    "translated_text": fields.String(attribute="translated_text"),
    "created_at": TimestampField(attribute="created_at"),
}


page_chat_message_fields = {
    "items": fields.List(fields.Nested(chat_message_fields)),
    "total": fields.Integer(attribute="total"),
    "page": fields.Integer(attribute="page"),
    "page_size": fields.Integer(attribute="page_size"),
}
