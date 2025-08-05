from flask_restful import fields
from ...libs.helper import TimestampField


app_partial_fields = {
    "id": fields.String(attribute="id"),
    "name": fields.String(attribute="name"),
    "description": fields.String(attribute="description"),
    # "mode": fields.String(attribute='mode')
    # "icon": fields.String(attribute='icon'),
    # "icon_background": fields.String(attribute='icon_background'),
    # "model_config": fields.Nested(
    #     model_config_partial_fields, attribute="app_model_config", allow_null=True
    # ),
    "createdAt": TimestampField(attribute="created_at"),
}


app_pagination_fields = {
    "page": fields.Integer,
    "limit": fields.Integer(attribute="per_page"),
    "total": fields.Integer,
    "hasMore": fields.Boolean(attribute="has_next"),
    "data": fields.List(fields.Nested(app_partial_fields), attribute="items"),
}
