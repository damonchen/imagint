from flask_restful import fields
from ...libs.helper import TimestampField

task_fields = {
    "id": fields.Integer(attribute="id"),
    "taskId": fields.String(attribute="task_id"),
    "userId": fields.Integer(attribute="user_id"),
    "status": fields.String(attribute="status"),
    "payload": fields.Raw(attribute="payload"),
    "result": fields.Raw(attribute="result"),
    "doneAt": TimestampField(attribute="done_at"),
    "createdBy": fields.Integer(attribute="created_by"),
    "createdAt": TimestampField(attribute="created_at"),
    "updatedBy": fields.Integer(attribute="updated_by"),
    "updatedAt": TimestampField(attribute="updated_at"),
}

partial_task_fields = {
    "id": fields.Integer(attribute="id"),
    "taskId": fields.String(attribute="task_id"),
    "userId": fields.Integer(attribute="user_id"),
    "status": fields.String(attribute="status"),
    "result": fields.Raw(attribute="result"),
    "doneAt": TimestampField(attribute="done_at"),
}

list_task_fields = fields.List(fields.Nested(task_fields))

task_pagination_fields = {
    "page": fields.Integer,
    "perPage": fields.Integer(attribute="per_page"),
    "total": fields.Integer,
    "hasMore": fields.Boolean(attribute="has_next"),
    "items": fields.List(fields.Nested(task_fields)),
}

task_status_fields = {
    "taskId": fields.String(attribute="task_id"),
    "status": fields.String(attribute="status"),
    "result": fields.Raw(attribute="result"),
    "done_at": TimestampField(attribute="done_at"),
}


dispatch_task_fields = {
    "taskId": fields.String(attribute="task_id"),
    "prompt": fields.String(attribute="prompt"),
    "params": fields.Raw(attribute="params"),
    "model": fields.String(),
    "type": fields.String(),
}
