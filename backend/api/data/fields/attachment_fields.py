from flask_restful import fields
from ...libs.helper import TimestampField


attachment_fields = {
    "id": fields.String(attribute="id"),
    "user_id": fields.String(attribute="user_id"),
    "containerId": fields.String(attribute="container_id"),
    "containerType": fields.String(attribute="container_type"),
    "filename": fields.String(attribute="filename"),
    "diskDirectory": fields.String(attribute="disk_directory"),
    "diskFilename": fields.String(attribute="disk_filename"),
    "fileSize": fields.Integer(attribute="file_size"),
    "contentType": fields.String(attribute="content_type"),
    "digest": fields.String(attribute="digest"),
    "description": fields.String(attribute="description"),
    "createdBy": fields.String(attribute="created_by"),
    "createdAt": TimestampField(attribute="created_at"),
    "updatedBy": fields.String(attribute="updated_by"),
    "updatedAt": TimestampField(attribute="updated_at"),
}
