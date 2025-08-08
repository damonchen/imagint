import json
import logging
import uuid
from typing import Optional
import datetime
from api.data.models.enums import AccountStatus
from api.data.models.account import Account
from api.services.errors.common import NotFoundError, ValidationError
from api.services.repository.account_repository import (
    AccountRepository,
    AccountPasswordTokenRepository,
)
from api.extensions.database import db
from api.extensions.mail import mail
from flask import render_template
from api.extensions.login import token_coder
from api.extensions.database import transaction
from api.services.redis_service import RedisService


class AccountService(object):

    @staticmethod
    def load_account(account_id: int) -> Account:
        """
        Load account by id
        """
        return AccountRepository.load_account(account_id)

    @staticmethod
    def load_account_by_email(email: str) -> Account:
        """
        Load account by email
        """
        return AccountRepository.load_account_by_email(email)

    @staticmethod
    def load_accounts():
        """
        Load all accounts
        """
        return AccountRepository.load_accounts()

    @staticmethod
    @transaction
    def register(
            email: str, username: str, password: str, invited_by: str = None
    ) -> dict:
        """
        Register new account

        Args:
            username: Account username
            password: Account password
            email: Account email

        Returns:
            Created account object

        Raises:
            ValidationError: If username/email already exists
        """
        # Check if username/email already exists
        # if AccountRepository.load_account_by_username(username):
        #     raise ValidationError("Username already exists")

        if AccountRepository.load_account_by_email(email):
            raise ValidationError("Email already exists")

        # Create account
        account = AccountRepository.create_account(
            username=username,
            password=password,
            email=email,
            invited_by=invited_by,
        )

        # send mail validate token
        mail_validate_token = AccountPasswordTokenRepository.create_token(
            account,
            type="register",
            expires_at=datetime.datetime.now(datetime.UTC)
                       + datetime.timedelta(hours=1),
        )

        RedisService.rpush("mail:account:register", json.dumps(
            {
                "id": account.id,
                "email": account.email,
                "token": mail_validate_token.token,
            },
        ))

        return account

    @staticmethod
    def active_account(account):
        return AccountRepository.update_account(account, status=AccountStatus.ACTIVE)

    @staticmethod
    def get_account_jwt_token(account: Account) -> str:
        """
        Get account JWT token
        """
        jwt_token = token_coder.encode(
            {
                "account_id": account.id,
                "email": account.email,
                "username": account.username,
            }
        )
        return jwt_token

    @staticmethod
    @transaction
    def login(email: str, password: str) -> Account:
        """
        Login account

        Args:
            email: Account email
            password: Account password

        Returns:
            Account object if login successful

        Raises:
            ValidationError: If login credentials invalid
        """
        account = AccountRepository.authenticate(email, password)
        return account

    @staticmethod
    @transaction
    def reset_password(email: str) -> None:
        """
        Initiate password reset flow

        Args:
            email: Account email

        Raises:
            NotFoundError: If account not found
        """
        account = AccountRepository.load_account_by_email(email)
        if not account:
            raise NotFoundError("Account not found")

        # Generate reset token and send email
        reset_token = AccountPasswordResetTokenRepository.create_token(account)

        # Send reset email via message queue
        html = render_template(
            "email/reset_password.html",
            reset_token=reset_token.token,
            account_id=account.id,
            email=email,
        )
        mail.send(to=email, subject="Reset Password", html=html)

    @staticmethod
    def send_reset_password_email(email: str, password: str) -> None:
        """
        Send reset password email
        """
        account = AccountRepository.load_account_by_email(email)
        if not account:
            raise NotFoundError("Account not found")

        AccountRepository.update_account(account, password=password)

    @staticmethod
    @transaction
    def confirm_reset_password(reset_token: str, new_password: str) -> None:
        """
        Complete password reset with token

        Args:
            reset_token: Password reset token
            new_password: New account password

        Raises:
            ValidationError: If reset token invalid
        """
        token = AccountPasswordTokenRepository.load_token(reset_token)
        if not token:
            raise ValidationError("Invalid or expired reset token")

        if token.is_expired:
            raise ValidationError("Invalid or expired reset token")

        account = AccountRepository.load_account(token.account_id)
        if not account:
            raise ValidationError("Invalid or expired reset token")

        # Update password
        AccountRepository.update_account(account, password=new_password)

        # Clear reset token
        AccountPasswordTokenRepository.delete_token(token)

    @staticmethod
    @transaction
    def change_password(
            account_id: int | Account, username: str, new_password: str
    ) -> Account:
        """
        Change account password

        Args:
            account_id: Account ID
            current_password: Current password
            new_password: New password

        Raises:
            ValidationError: If current password invalid
        """
        if isinstance(account_id, int):
            account = AccountRepository.load_account(account_id)
        else:
            account = account_id

        if not account:
            raise NotFoundError("Account not found")

        # if not account.check_password(current_password):
        #     raise ValidationError("Current password is incorrect")

        account = AccountRepository.update_account(
            account, username=username, password=new_password
        )

        db.session.commit()
        return account
