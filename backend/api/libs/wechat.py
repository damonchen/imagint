import logging
from flask import g, make_response, request, session, redirect, url_for
from api.extensions.wechat import wechat_oauth


def get_authorize_url():
    redirect_uri = url_for("wechat.authorized", next=request.full_path, _external=True)
    params = dict(
        redirect_uri=redirect_uri,
        scope="snapi_userinfo",
    )
    return wechat_oauth.get_authorize_url(**params)
