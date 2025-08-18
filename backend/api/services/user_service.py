import json
import logging
import uuid
from typing import Optional
import datetime
from api.data.models.enums import UserStatus
from api.data.models.user import User
from api.services.errors.common import NotFoundError, ValidationError
from api.services.repository.user_repository import (
    UserRepository,
    UserPasswordTokenRepository,
    AccountRepository,
    UserLocationEvidenceRepository,
)
from api.services.credit_service import UserCreditService
from api.extensions.database import db
from api.extensions.mail import mail
from flask import render_template
from api.extensions.login import token_coder
from api.extensions.database import transaction
from api.services.redis_service import RedisService


class UserService(object):

    @staticmethod
    def load_user(user_id: int) -> User:
        """
        Load user by id
        """
        return UserRepository.load_user(user_id)

    @staticmethod
    def load_user_by_email(email: str) -> User:
        """
        Load user by email
        """
        return UserRepository.load_user_by_email(email)

    @staticmethod
    def load_users():
        """
        Load all users
        """
        return UserRepository.load_users()

    @staticmethod
    @transaction
    def register(
        email: str, username: str, password: str, invited_by: str = None
    ) -> dict:
        """
        Register new user

        Args:
            username: User username
            password: User password
            email: User email

        Returns:
            Created user object

        Raises:
            ValidationError: If username/email already exists
        """
        # Check if username/email already exists
        # if UserRepository.load_user_by_username(username):
        #     raise ValidationError("Username already exists")

        if UserRepository.load_user_by_email(email):
            raise ValidationError("Email already exists")

        # Create user
        user = UserRepository.create_user(
            username=username,
            password=password,
            email=email,
            invited_by=invited_by,
        )

        # send mail validate token
        mail_validate_token = UserPasswordTokenRepository.create_token(
            user,
            type="register",
            expires_at=datetime.datetime.now(datetime.UTC)
            + datetime.timedelta(hours=1),
        )

        RedisService.rpush(
            "mail:user:register",
            json.dumps(
                {
                    "id": user.id,
                    "email": user.email,
                    "token": mail_validate_token.token,
                },
            ),
        )

        # Initialize credit for the new user
        UserCreditService.initialize_user_credits(user)

        return user

    @staticmethod
    def active_user(user):
        return UserRepository.update_user(user, status=UserStatus.ACTIVE)

    @staticmethod
    def get_user_jwt_token(user: User) -> str:
        """
        Get user JWT token
        """
        jwt_token = token_coder.encode(
            {
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
            }
        )
        return jwt_token

    @staticmethod
    @transaction
    def login(email: str, password: str) -> User:
        """
        Login user

        Args:
            email: User email
            password: User password

        Returns:
            User object if login successful

        Raises:
            ValidationError: If login credentials invalid
        """
        user = UserRepository.authenticate(email, password)
        return user

    @staticmethod
    @transaction
    def reset_password(email: str) -> None:
        """
        Initiate password reset flow

        Args:
            email: User email

        Raises:
            NotFoundError: If user not found
        """
        user = UserRepository.load_user_by_email(email)
        if not user:
            raise NotFoundError("User not found")

        # Generate reset token and send email
        reset_token = UserPasswordTokenRepository.create_token(user)

        # Send reset email via message queue
        html = render_template(
            "email/reset_password.html",
            reset_token=reset_token.token,
            user_id=user.id,
            email=email,
        )
        mail.send(to=email, subject="Reset Password", html=html)

    @staticmethod
    def send_reset_password_email(email: str, password: str) -> None:
        """
        Send reset password email
        """
        user = UserRepository.load_user_by_email(email)
        if not user:
            raise NotFoundError("User not found")

        UserRepository.update_user(user, password=password)

    @staticmethod
    @transaction
    def confirm_reset_password(reset_token: str, new_password: str) -> None:
        """
        Complete password reset with token

        Args:
            reset_token: Password reset token
            new_password: New user password

        Raises:
            ValidationError: If reset token invalid
        """
        token = UserPasswordTokenRepository.load_token(reset_token)
        if not token:
            raise ValidationError("Invalid or expired reset token")

        if token.is_expired:
            raise ValidationError("Invalid or expired reset token")

        user = UserRepository.load_user(token.user_id)
        if not user:
            raise ValidationError("Invalid or expired reset token")

        # Update password
        UserRepository.update_user(user, password=new_password)

        # Clear reset token
        UserPasswordTokenRepository.delete_token(token)

    @staticmethod
    @transaction
    def change_password(user_id: int | User, username: str, new_password: str) -> User:
        """
        Change user password

        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password

        Raises:
            ValidationError: If current password invalid
        """
        if isinstance(user_id, int):
            user = UserRepository.load_user(user_id)
        else:
            user = user_id

        if not user:
            raise NotFoundError("User not found")

        # if not user.check_password(current_password):
        #     raise ValidationError("Current password is incorrect")

        user = UserRepository.update_user(
            user, username=username, password=new_password
        )

        db.session.commit()
        return user


class AccountService(object):

    @staticmethod
    def load_account(user: User) -> dict:
        return AccountRepository.load_account(user)

    @staticmethod
    @transaction
    def create_or_update_account(user: User, **kwargs) -> dict:
        return AccountRepository.create_or_update_account(user, **kwargs)

    @staticmethod
    def get_account_balance(user: User) -> float:
        account = AccountRepository.load_account(user)
        if not account:
            return 0.0
        return account.balance


class UserLocationEvidenceService(object):

    @staticmethod
    def create_location_evidence(user: User, type: str, data: dict) -> None:
        """
        Create a new location evidence for the user
        """
        return UserLocationEvidenceRepository.create_user_location_evidence(
            user, type, data
        )

    @staticmethod
    def create_ip_evidence(user: User, ip: str) -> None:
        """
        Create a new IP evidence for the user
        """
        return UserLocationEvidenceRepository.create_user_location_evidence(
            user, "ip", {"ip": ip}
        )

    @staticmethod
    def list_location_evidences(user: User) -> list:
        """
        List all location evidences for the user
        """
        return UserLocationEvidenceRepository.load_user_location_evidences(user)
