from flask import Blueprint
from api.libs.external_api import ExternalApi

# 开放给第三方使用的接口
bp = Blueprint("service_api", __name__, url_prefix="/v1")
api = ExternalApi(bp)

from . import index
from . import user
from . import audit
from . import auth
from . import chat
from . import subscription
from . import task
from . import file
from . import transaction
from . import credit
