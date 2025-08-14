from flask_restful import fields

from ...libs.helper import TimestampField

upload_config_fields = {
    "fileSizeLimit": fields.Integer(attribute="file_size_limit"),
    "imageFileSizeLimit": fields.Integer(attribute="image_file_size_limit"),
}

file_fields = {
    "id": fields.String(attribute="id"),
    "name": fields.String(attribute="name"),
    "size": fields.String(attribute="size"),
    "extension": fields.String(attribute="extension"),
    "digest": fields.String(attribute="digest"),
    "mimeType": fields.String(attribute="mime_type"),
    "createdBy": fields.String(attribute="created_by"),
    "createdAt": TimestampField(attribute="created_at"),
}

attachment_fields = {
    "id": fields.Integer(attribute="id"),
    "file_id": fields.String(attribute="file_id"),
    "userId": fields.Integer(attribute="user_id"),
    "originalName": fields.String(attribute="original_name"),
    # "storage_path": fields.String(attribute="storage_path"),
    "fileSize": fields.Integer(attribute="file_size"),
    "mimeType": fields.String(attribute="mime_type"),
    "digest": fields.String(attribute="digest"),
    "description": fields.String(attribute="description"),
    "status": fields.String(attribute="status"),
    "createdBy": fields.Integer(attribute="created_by"),
    "createdAt": TimestampField(attribute="created_at"),
    "updatedBy": fields.Integer(attribute="updated_by"),
    "updatedAt": TimestampField(attribute="updated_at"),
}


list_attachment_fields = {"items": fields.List(fields.Nested(attachment_fields))}


attachment_file_fields = {
    "fileId": fields.String(attribute="file_id"),
    "url": fields.String(attribute="url"),
}


list_attachment_file_fields = {
    "items": fields.List(fields.Nested(attachment_file_fields))
}
