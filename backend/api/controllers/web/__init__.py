from flask import Blueprint
from api.libs.external_api import ExternalApi

# 自己的web和app使用的接口
bp = Blueprint("web", __name__, url_prefix="/v1")
api = ExternalApi(bp)
