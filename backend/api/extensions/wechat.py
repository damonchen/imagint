import copy
from urllib.parse import urlencode
import requests


class WechatOauth(object):
    # see https://developers.weixin.qq.com/doc/oplatform/Website_App/WeChat_Login/Wechat_Login.html
    authorize_url = "https://open.weixin.qq.com/connect/oauth2/authorize"
    base_url = "https://api.weixin.qq.com/sns/"

    def __init__(self, app=None, app_id=None, app_secret=None) -> None:
        self.app_id = app_id
        self.app_secret = app_secret
        self.code = ""
        self.state = ""
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        if not self.app_id:
            self.app_id = app.config.get("WECHAT_APP_ID")

        if not self.app_secret:
            self.app_secret = app.config.get("WECHAT_APP_SECRET")

    def get_authorize_url(self, redirect_uri, scope="snapi_base", **kwargs):
        params = copy.deepcopy(kwargs)
        params.update(
            {
                "appid": self.app_id,
                "response_type": "code",
                "scope": scope,
                "redirect_uri": redirect_uri,
            }
        )
        query = urlencode(sorted(params.items()))

        return f"{self.authorize_url}?{query}#wechat_redirect"

    def get_access_token(self, code):
        """
        正确的返回数据
        {
            "access_token":"ACCESS_TOKEN",
            "expires_in":7200,
            "refresh_token":"REFRESH_TOKEN","openid":"OPENID",
            "scope":"SCOPE"
        }"""
        url = f"{self.base_url}/oauth2/access_token"

        params = {
            "appid": self.app_id,
            "secret": self.app_secret,
            "code": code,
            "grant_type": "authorization_code",
        }
        r = requests.get(url, params=params)
        return r.json()

    def refresh_token(self, refresh_token):
        """
        正确的返回：
        {
            "access_token":"ACCESS_TOKEN",
            "expires_in":7200,
            "refresh_token":"REFRESH_TOKEN",
            "openid":"OPENID",
            "scope":"SCOPE"
        }
        """
        url = f"{self.base_url}/oauth2/refresh_token"
        params = {
            "appid": self.app_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        r = requests.get(url, params=params)
        return r.json()

    def valid_access_token(self, access_token, open_id):
        """
        正确结果：
         {
            "errcode":0,
            "errmsg":"ok"
        }
        错误结果：
        {
            "errcode":40003,
            "errmsg":"invalid openid"
        }
        """
        url = f"{self.base_url}/auth"
        params = {"access_token": access_token, "openid": open_id}
        r = requests.get(url, params=params)
        return r.json()

    def get_userinfo(self, access_token, open_id):
        """正确返回结果：
        {
            "openid":"OPENID",
            "nickname":"NICKNAME",
            "sex":1,
            "province":"PROVINCE",
            "city":"CITY",
            "country":"COUNTRY",
            "headimgurl": "头像url",
            "privilege":[
                "PRIVILEGE1",
                "PRIVILEGE2"
            ],
            "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
        }
        """

        url = f"{self.base_url}/userinfo"
        params = {"access_token": access_token, "openid": open_id}
        r = requests.get(url, params=params)
        if r.encoding == "IOS-8859-1":
            r.encoding = "utf-8"
        return r.json()


wechat_oauth = WechatOauth()


def init_app(app):
    wechat_oauth.init_app(app)
