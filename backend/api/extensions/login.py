import jwt
from werkzeug.exceptions import Unauthorized
import flask_login


class TokenCoder(object):

    def __init__(self, app=None):
        self.app = app
        self.sk = ""
        if app is not None:
            self.sk = app.config.get("SECRET_KEY")

    def init_app(self, app):
        self.app = app
        self.sk = app.config.get("SECRET_KEY")

    def encode(self, payload):
        return jwt.encode(payload, self.sk, algorithm="HS256")

    def decode(self, token):
        try:
            return jwt.decode(token, self.sk, algorithms=["HS256"])
        except jwt.exceptions.InvalidSignatureError:
            raise Unauthorized("Invalid token signature.")
        except jwt.exceptions.DecodeError:
            raise Unauthorized("Invalid token.")
        except jwt.exceptions.ExpiredSignatureError:
            raise Unauthorized("Token has expired.")


token_coder = TokenCoder()
login_manager = flask_login.LoginManager()


def init_app(app):
    login_manager.init_app(app)
    token_coder.init_app(app)
