import logging
import datetime
from datetime import timedelta
from flask import current_app
from jinja2 import Environment, FileSystemLoader, select_autoescape
from api.data.models.user import (
    User,
    Account,
    UserPasswordToken,
    UserLocationEvidence,
)
from api.services.captcha_service import CaptchaService
from api.libs.password import compare_password

from api.data.models.enums import (
    UserStatus,
)
from api.extensions.database import db
from api.extensions.mail import mail
from api.libs.exceptions import UserLoginError
from api.libs.password import (
    hash_password,
    generate_password_salt,
    generate_password_reset_token,
)
from api.services.errors.user import RegisterError
from api.services.errors.common import NotFoundError

logger = logging.getLogger("services.user")


class UserRepository(object):

    @staticmethod
    def load_user(user_id):
        if isinstance(user_id, User):
            return user_id

        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return None

        return user

    @staticmethod
    def load_users():
        users = User.query.all()
        return users

    @staticmethod
    def load_user_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user

    # def get_user_jwt_token(self):
    #     expired_datetime = datetime.datetime.now(datetime.UTC) + timedelta(days=1)
    #     timestamp = expired_datetime.timestamp()
    #     payload = {
    #         "user_id": self.id,
    #         "exp": timestamp,
    #         "sub": self.email,
    #     }

    #     token = token_coder.encode(payload)
    #     return token

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()
        if user is None:
            logger.error("user not exist")
            raise UserLoginError("Invalid email or password")

        if user.is_not_valid:
            logger.error("user is not valid")
            raise UserLoginError("User is banned or closed.")

        if not user.is_active:
            logger.error("user is not active")
            raise UserLoginError("User should be active")

        if not user.check_password(password):
            logger.error("check password failed")
            raise UserLoginError("Invalid email or password")

        user.last_login_at = datetime.datetime.now(datetime.UTC)
        db.session.add(user)

        return user

    @staticmethod
    def authenticate_mobile(mobile, captcha) -> User:
        user = User.query.filter_by(mobile=mobile).first()
        if user is None:
            raise UserLoginError("Invalid mobile or captcha")

        if user.is_not_valid:
            raise UserLoginError("User is banned or closed.")

        CaptchaService.valid_captcha_code(mobile, captcha)

        return user

    @staticmethod
    def send_reset_password_code(user) -> None:
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

        mail.send(user.email, "Reset Password", html, mail_from)

    @staticmethod
    def is_unique_email(email):
        # 确认系统只有一个email
        count = db.session.query(User).filter(User.email == email).count()
        return count == 0

    @staticmethod
    def create_user(
        email,
        username,
        password,
        invited_by=None,
        timezone="Asia/Shanghai",
    ) -> User:
        if not UserRepository.is_unique_email(email):
            raise RegisterError()

        user = User(
            email=email,
            username=username,
            timezone=timezone,
            invited_by=invited_by,
            status=str(UserStatus.PENDING),
        )
        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        return user

    @staticmethod
    def active_user(user):
        user.status = UserStatus.ACTIVE.value
        user.updated_by = user.id

        db.session.add(user)
        db.session.flush()

        return user

    @staticmethod
    def update_user(user, **kwargs) -> User:
        for key, value in kwargs.items():
            if key == "password":
                salt = generate_password_salt()
                hashed_password = hash_password(value, bytes.fromhex(salt))
                user.password = hashed_password
            else:
                setattr(user, key, value)

        db.session.add(user)
        db.session.flush()

        return user


class UserPasswordTokenRepository(object):
    @staticmethod
    def create_token(user, type, expires_at):
        token = UserPasswordToken(
            user_id=user.id,
            type=type,
            token=generate_password_reset_token(),
            expires_at=expires_at,
        )
        db.session.add(token)
        db.session.flush()

        return token

    @staticmethod
    def load_token(token):
        return UserPasswordToken.query.filter_by(token=token).first()

    @staticmethod
    def delete_token(token):
        db.session.delete(token)
        db.session.flush()


class AccountRepository(object):

    @staticmethod
    def load_account(self, user):
        return db.session.query(Account).filter_by(user_id=user.id).first()

    @staticmethod
    def create_or_update_account(self, user, **kwargs):
        account = db.session.query(Account).filter_by(user_id=user.id).first()
        if not account:
            account = Account(user_id=user.id)
            db.session.add(account)
            db.session.flush()

        for key, value in kwargs.items():
            setattr(account, key, value)

        db.session.add(account)
        db.session.flush()
        return account

    @staticmethod
    def delete_account(self, user):
        db.session.query(Account).filter_by(user_id=user.id).delete()


class UserLocationEvidenceRepository(object):

    @staticmethod
    def create_user_location_evidence(user, type, data):
        user_location = UserLocationEvidence(user_id=user.id, type=type, data=data)
        db.session.add(user_location)
        db.session.flush()

        return user_location

    @staticmethod
    def load_user_location_evidences(user):
        return (
            db.session.query(UserLocationEvidence)
            .filter(UserLocationEvidence.user_id == user.id)
            .all()
        )

    @staticmethod
    def load_user_location_evidence(user, id):
        return (
            db.session.query(UserLocationEvidence)
            .filter(UserLocationEvidence.user_id == user.id)
            .filter(UserLocationEvidence.id == id)
            .first()
        )
