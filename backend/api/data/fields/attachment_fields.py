from flask_restful import fields
from ...libs.helper import TimestampField


attachment_fields = {
    "id": fields.String(attribute="id"),
    "user_id": fields.String(attribute="user_id"),
    "container_id": fields.String(attribute="container_id"),
    "container_type": fields.String(attribute="container_type"),
    "filename": fields.String(attribute="filename"),
    "disk_directory": fields.String(attribute="disk_directory"),
    "disk_filename": fields.String(attribute="disk_filename"),
    "file_size": fields.Integer(attribute="file_size"),
    "content_type": fields.String(attribute="content_type"),
    "digest": fields.String(attribute="digest"),
    "description": fields.String(attribute="description"),
    "created_by": fields.String(attribute="created_by"),
    "created_at": TimestampField(attribute="created_at"),
    "updated_by": fields.String(attribute="updated_by"),
    "updated_at": TimestampField(attribute="updated_at"),
}
