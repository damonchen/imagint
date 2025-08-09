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
    "pageSize": fields.Integer(attribute="page_size"),
}

chat_message_image_fields = {
    "id": fields.String(attribute="id"),
    "chatMessageId": fields.String(attribute="chat_message_id"),
    "imagePath": fields.String(attribute="image_path"),
}

chat_message_fields = {
    "id": fields.String(attribute="id"),
    "chatId": fields.String(attribute="chat_id"),
    "type": fields.String(attribute="type"),
    "prompt": fields.String(attribute="prompt"),
    "params": fields.Raw(attribute="params"),
    "status": fields.String(attribute="status"),
    "imagePath": fields.String(attribute="image_path"),
    "imageCount": fields.Integer(attribute="image_count"),
    "images": fields.List(fields.Nested(chat_message_image_fields)),
    "createdAt": TimestampField(attribute="created_at"),
}


page_chat_message_fields = {
    "items": fields.List(fields.Nested(chat_message_fields)),
    "total": fields.Integer(attribute="total"),
    "page": fields.Integer(attribute="page"),
    "pageSize": fields.Integer(attribute="page_size"),
}
