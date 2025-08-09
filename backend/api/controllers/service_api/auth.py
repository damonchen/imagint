import json
import logging
from flask_restful import Resource, reqparse
from api.libs.exceptions import AccountLoginError, NotFoundError
from api.services.captcha_service import CaptchaService
from api.services.errors.account import RegisterError
from api.extensions.redis import redis_client
from .errors import CreatedAccountError, AuthenticationError
from api.services.account_service import AccountService
from . import api

logger = logging.getLogger("web/auth")


class IndexResource(Resource):

    def get(self):
        return {"hello": "world"}


class AuthInvitedCode(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("invitedCode", type=str, location="param")

        args = parser.parse_args()
        invited_code = args.invitedCode
        user_id = redis_client.get(invited_code)

        return {"validate": bool(user_id)}


class AuthPasswordRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, location="json")
        parser.add_argument("username", type=str, location="json")
        parser.add_argument("password", type=str, location="json")
        parser.add_argument("invitedCode", type=str, location="json", required=False)

        args = parser.parse_args()

        email = args.email
        password = args.password
        username = args.username
        # TODO: checkout password

        invited_code = args.invitedCode
        if invited_code:
            invited_obj = redis_client.get(f"invite/{invited_code}")
            if not invited_obj:
                # raise RegisterError("not validate error")
                account_id = None
            else:
                try:
                    invited_obj = json.loads(invited_obj)
                    account_id = invited_obj["account_id"]
                except Exception as e:
                    logger.warning("register account error occur for json loads", e)
                    account_id = None
        else:
            account_id = None

        try:
            account = AccountService.register(
                email=email,
                username=username,
                password=password,
                invited_by=account_id,
                language="zh-CN",
                theme="light",
            )
        except RegisterError as e:
            raise CreatedAccountError

        if account is not None:
            token = AccountService.get_account_jwt_token(account)
        else:
            token = None

        return {
            "access_token": token,
        }


class AuthPasswordLogin(Resource):

    def post(self):
        print("auth password login")
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, location="json")
        parser.add_argument("password", type=str, location="json")

        args = parser.parse_args()

        email = args.email
        password = args.password

        try:
            account = AccountService.login(email, password)
        except AccountLoginError as e:
            logger.error("account login error %s", e)
            raise AuthenticationError()

        if account is None:
            raise NotFoundError("Account not found")

        token = AccountService.get_account_jwt_token(account)

        # return make_response(token, 200)
        return {
            "access_token": token,
        }


class AuthLogout(Resource):

    def post(self):
        return {}


class AuthPasswordReset(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, location="json")
        args = parser.parse_args()

        email = args.email
        AccountService.reset_password(email)
        return {}


class AuthPasswordResetConfirm(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, location="json")
        parser.add_argument("password", type=str, location="json")
        args = parser.parse_args()

        email = args.email
        password = args.password
        account = AccountService.confirm_reset_password(email, password)

        return {
            "access_token": AccountService.get_account_jwt_token(account),
        }


class AuthPasswordChange(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, location="json")
        parser.add_argument("password", type=str, location="json")
        args = parser.parse_args()

        email = args.email
        password = args.password
        account = AccountService.change_password(email, password)

        return {
            "access_token": AccountService.get_account_jwt_token(account),
        }


class AuthCaptcha(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("mobile", type=str, location="json")
        args = parser.parse_args()

        mobile = args.mobile
        CaptchaService.send_captcha_code(mobile)
        return {}


class AuthCaptchaVerify(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("mobile", type=str, location="json")
        parser.add_argument("captcha", type=str, location="json")
        args = parser.parse_args()

        mobile = args.mobile
        captcha = args.captcha
        CaptchaService.valid_captcha_code(mobile, captcha)
        return {}


api.add_resource(IndexResource, "/")
api.add_resource(AuthPasswordRegister, "/auth/signup")
api.add_resource(AuthPasswordLogin, "/auth/login")
api.add_resource(AuthPasswordReset, "/auth/password/reset")
api.add_resource(AuthPasswordResetConfirm, "/auth/password/reset/confirm")
api.add_resource(AuthPasswordChange, "/auth/password/change")
api.add_resource(AuthLogout, "/auth/logout")
api.add_resource(AuthCaptcha, "/auth/captcha")
api.add_resource(AuthCaptchaVerify, "/auth/captcha/verify")
