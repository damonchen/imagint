from flask_restful import fields
from ...libs.helper import TimestampField

task_fields = {
    "id": fields.Integer(attribute="id"),
    "task_id": fields.String(attribute="task_id"),
    "account_id": fields.Integer(attribute="account_id"),
    "status": fields.String(attribute="status"),
    "payload": fields.Raw(attribute="payload"),
    "result": fields.Raw(attribute="result"),
    "done_at": TimestampField(attribute="done_at"),
    "created_by": fields.Integer(attribute="created_by"),
    "created_at": TimestampField(attribute="created_at"),
    "updated_by": fields.Integer(attribute="updated_by"),
    "updated_at": TimestampField(attribute="updated_at"),
}

partial_task_fields = {
    "id": fields.Integer(attribute="id"),
    "task_id": fields.String(attribute="task_id"),
    "account_id": fields.Integer(attribute="account_id"),
    "status": fields.String(attribute="status"),
    "result": fields.Raw(attribute="result"),
    "done_at": TimestampField(attribute="done_at"),
}

list_task_fields = fields.List(fields.Nested(task_fields))

task_pagination_fields = {
    "page": fields.Integer,
    "per_page": fields.Integer(attribute="per_page"),
    "total": fields.Integer,
    "hasMore": fields.Boolean(attribute="has_next"),
    "items": fields.List(fields.Nested(task_fields)),
}

task_status_fields = {
    "task_id": fields.String(attribute="task_id"),
    "status": fields.String(attribute="status"),
    "result": fields.Raw(attribute="result"),
    "done_at": TimestampField(attribute="done_at"),
}


dispatch_task_fields = {
    "task_id": fields.String(attribute="task_id"),
    "prompt": fields.String(attribute="prompt"),
    "params": fields.Raw(attribute="params"),
}
