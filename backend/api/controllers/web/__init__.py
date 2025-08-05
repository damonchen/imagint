from flask import Blueprint
from api.libs.external_api import ExternalApi

# 自己的web和app使用的接口
bp = Blueprint("web", __name__, url_prefix="/v1")
api = ExternalApi(bp)

from . import index
from . import account
from . import audit
from . import auth
from . import subscription
from . import task
from . import chat
from . import file


bp.add_url_rule("/files/<file_id>", view_func=file.get_attachment, methods=["GET"])
