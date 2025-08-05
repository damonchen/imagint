import logging
from os import access
import re
from weakref import ref
from flask import Blueprint, request, redirect, session, jsonify
from api.extensions.wechat import wechat_oauth
from api.libs.decorator import openid_required

logger = logging.getLogger("wechat")

bp = Blueprint("wechat", __name__)

# 二维码授权登录码
# https://open.weixin.qq.com/connect/qrconnect?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect


@bp.route("/authorized")
def index():
    code = request.args.get("code")
    next_ = request.args.get("next", "/")
    if not code:
        logger.warning("code not found")
        pass

    resp_data = wechat_oauth.get_access_token(code)

    openid = resp_data["openid"]
    access_token = resp_data["access_token"]
    refresh_token = resp_data["refresh_token"]

    session["openid"] = openid
    session["access_token"] = access_token
    session["refresh_token"] = refresh_token

    return redirect(next_)


@bp.route("/refresh-token")
@openid_required
def refresh_token():
    refresh_token = session["refresh_token"]
    resp_data = wechat_oauth.refresh_token(refresh_token)

    openid = resp_data["openid"]
    access_token = resp_data["access_token"]
    refresh_token = resp_data["refresh_token"]

    session["openid"] = openid
    session["access_token"] = access_token
    session["refresh_token"] = refresh_token

    return jsonify(resp_data)


@bp.route("/check-access-token")
@openid_required
def valid_check_access_token():
    access_token = session["access_token"]
    openid = session["openid"]
    result = wechat_oauth.valid_access_token(access_token, openid)
    return jsonify(result)


@bp.route("/userinfo", methods=["GET", "POST"])
@openid_required
def userinfo():
    access_token = session["access_token"]
    openid = session["openid"]
    info = wechat_oauth.get_userinfo(access_token, openid)
    return jsonify(info)
