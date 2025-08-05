from flask import Blueprint
from libs.external_api import ExternalApi

bp = Blueprint("console", __name__, url_prefix="/console/api")
api = ExternalApi(bp)

from . import version, ping
