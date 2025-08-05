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
    "mime_type": fields.String(attribute="mime_type"),
    "created_by": fields.String(attribute="created_by"),
    "created_at": TimestampField(attribute="created_at"),
}

attachment_fields = {
    "id": fields.Integer(attribute="id"),
    "file_id": fields.String(attribute="file_id"),
    "account_id": fields.Integer(attribute="account_id"),
    "original_name": fields.String(attribute="original_name"),
    # "storage_path": fields.String(attribute="storage_path"),
    "file_size": fields.Integer(attribute="file_size"),
    "mime_type": fields.String(attribute="mime_type"),
    "digest": fields.String(attribute="digest"),
    "description": fields.String(attribute="description"),
    "status": fields.String(attribute="status"),
    "created_by": fields.Integer(attribute="created_by"),
    "created_at": TimestampField(attribute="created_at"),
    "updated_by": fields.Integer(attribute="updated_by"),
    "updated_at": TimestampField(attribute="updated_at"),
}


list_attachment_fields = {"items": fields.List(fields.Nested(attachment_fields))}


attachment_file_fields = {
    "file_id": fields.String(attribute="file_id"),
    "url": fields.String(attribute="url"),
}


list_attachment_file_fields = {
    "items": fields.List(fields.Nested(attachment_file_fields))
}
