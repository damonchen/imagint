import logging
import datetime
from datetime import timedelta
from flask import current_app
from jinja2 import Environment, FileSystemLoader, select_autoescape
from api.data.models.account import (
    Account,
    AccountPasswordToken,
)
from api.services.captcha_service import CaptchaService
from api.libs.password import compare_password

from api.data.models.enums import (
    AccountStatus,
)
from api.extensions.database import db
from api.extensions.mail import mail
from api.libs.exceptions import AccountLoginError
from api.libs.password import (
    hash_password,
    generate_password_salt,
    generate_password_reset_token,
)
from api.services.errors.account import RegisterError
from api.services.errors.common import NotFoundError

logger = logging.getLogger("services.account")


class AccountRepository(object):

    @staticmethod
    def load_account(account_id):
        if isinstance(account_id, Account):
            return account_id

        account = Account.query.filter_by(id=account_id).first()
        if account is None:
            return None

        return account

    @staticmethod
    def load_accounts():
        accounts = Account.query.all()
        return accounts

    @staticmethod
    def load_account_by_email(email):
        account = Account.query.filter_by(email=email).first()
        return account

    # def get_account_jwt_token(self):
    #     expired_datetime = datetime.datetime.now(datetime.UTC) + timedelta(days=1)
    #     timestamp = expired_datetime.timestamp()
    #     payload = {
    #         "account_id": self.id,
    #         "exp": timestamp,
    #         "sub": self.email,
    #     }

    #     token = token_coder.encode(payload)
    #     return token

    @staticmethod
    def authenticate(email, password):
        account = Account.query.filter_by(email=email).first()
        if account is None:
            logger.error("account not exist")
            raise AccountLoginError("Invalid email or password")

        if account.is_not_valid:
            logger.error("account is not valid")
            raise AccountLoginError("Account is banned or closed.")

        if not account.is_active:
            logger.error("account is not active")
            raise AccountLoginError("Account should be active")

        if not account.check_password(password):
            logger.error("check password failed")
            raise AccountLoginError("Invalid email or password")

        account.last_login_at = datetime.datetime.now(datetime.UTC)
        db.session.add(account)

        return account

    @staticmethod
    def authenticate_mobile(mobile, captcha) -> Account:
        account = Account.query.filter_by(mobile=mobile).first()
        if account is None:
            raise AccountLoginError("Invalid mobile or captcha")

        if account.is_not_valid:
            raise AccountLoginError("Account is banned or closed.")

        CaptchaService.valid_captcha_code(mobile, captcha)

        return account

    @staticmethod
    def send_reset_password_code(account) -> None:
        mail_from = current_app.config.get("MAIL_DEFAULT_SEND_FROM")
        ctx = {
            "to": "",
            "inviter_name": "",
            "site_name": "",
            "url": "",
        }
        env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(),
        )
        template = env.get_template("")
        html = template.render(ctx)

        mail.send(account.email, "Reset Password", html, mail_from)

    @staticmethod
    def is_unique_email(email):
        # 确认系统只有一个email
        count = db.session.query(Account).filter(Account.email == email).count()
        return count == 0

    @staticmethod
    def create_account(
        email,
        username,
        password,
        language=None,
        theme=None,
        invited_by=None,
        timezone="Asia/Shanghai",
    ) -> Account:
        if not AccountRepository.is_unique_email(email):
            raise RegisterError()

        account = Account(
            email=email,
            username=username,
            language=language,
            theme=theme,
            timezone=timezone,
            invited_by=invited_by,
            status=str(AccountStatus.PENDING),
        )
        account.set_password(password)

        db.session.add(account)
        db.session.flush()

        return account

    @staticmethod
    def active_account(account):
        account.status = AccountStatus.ACTIVE.value
        account.updated_by = account.id
        db.session.add(account)
        db.session.flush()

        return account

    @staticmethod
    def update_account(account, **kwargs) -> Account:
        for key, value in kwargs.items():
            if key == "password":
                salt = generate_password_salt()
                hashed_password = hash_password(value, bytes.fromhex(salt))
                account.password = hashed_password
            else:
                setattr(account, key, value)
        db.session.add(account)
        db.session.flush()
        return account


class AccountPasswordTokenRepository(object):
    @staticmethod
    def create_token(account, type, expires_at):
        token = AccountPasswordToken(
            account_id=account.id,
            type=type,
            token=generate_password_reset_token(),
            expires_at=expires_at,
        )
        db.session.add(token)
        db.session.flush()

        return token

    @staticmethod
    def load_token(token):
        return AccountPasswordToken.query.filter_by(token=token).first()

    @staticmethod
    def delete_token(token):
        db.session.delete(token)
        db.session.flush()
