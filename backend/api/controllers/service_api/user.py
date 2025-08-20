import logging
from flask_restful import marshal_with, reqparse
from api.libs.decorator import manager_required
from api.data.fields.user_fields import (
    list_user_fields,
    user_partial_fields,
)
from api.services.errors.common import ValidationError
from api.services.user_service import UserService

from . import api
from .wraps import WebApiResource
from api.libs.decorator import unified_response
from api.libs.response import make_response


class UsersResource(WebApiResource):
    # 越是基础的，越需要放到最后面，这个是实现依赖

    @manager_required
    @unified_response(list_user_fields)
    def get(self, user):
        users = UserService.load_users()
        return make_response(users)


class UserResource(WebApiResource):

    @manager_required
    @unified_response(user_partial_fields)
    def get(self, user, pk):
        user = UserService.load_user(pk)
        return make_response(user)


class UserSelfResource(WebApiResource):

    @unified_response(user_partial_fields)
    def get(self, user):
        return make_response(user)

    @unified_response(user_partial_fields)
    def put(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, location="json")
        parser.add_argument("password", type=str, location="json")
        args = parser.parse_args()

        username = args.username
        password = args.password

        return make_response(
            UserService.change_password(
                user,
                username=username,
                password=password,
            )
        )


class UserSelfChangePasswordResource(WebApiResource):

    @unified_response(user_partial_fields)
    def post(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument("oldPassword", type=str, location="json")
        parser.add_argument("newPassword", type=str, location="json")
        parser.add_argument("confirmedNewPassword", type=str, location="json")
        args = parser.parse_args()

        old_password = args.oldPassword
        new_password = args.newPassword
        confirmed_new_password = args.confirmedNewPassword

        if new_password != confirmed_new_password:
            return make_response(
                status="failed",
                message="New password and confirmed new password do not match",
            )

        try:
            resp = UserService.change_password(
                user,
                username=user.username,
                old_password=old_password,
                new_password=new_password,
            )
            return make_response(resp)
        except ValidationError as e:
            return make_response(
                status="failed",
                message=str(e),
            )


class UserSelfUpdateProfileResource(WebApiResource):

    @unified_response(user_partial_fields)
    def post(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, location="json")
        args = parser.parse_args()

        username = args.username

        return make_response(
            UserService.update_profile(
                user,
                username=username,
            )
        )


class UserSelfAppearanceResource(WebApiResource):

    @unified_response(user_partial_fields)
    def post(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument("theme", type=str, location="json")
        args = parser.parse_args()

        theme = args.theme

        return make_response(
            UserService.update_appearance(
                user,
                theme=theme,
            )
        )


api.add_resource(UserSelfResource, "/self")
api.add_resource(UserSelfChangePasswordResource, "/self/change-password")
api.add_resource(UserSelfUpdateProfileResource, "/self/update-profile")
api.add_resource(UserSelfAppearanceResource, "/self/appearance")

api.add_resource(UsersResource, "/users")
api.add_resource(UserResource, "/users/<pk>")
