import logging
from flask_restful import marshal_with, reqparse
from api.libs.decorator import manager_required
from api.data.fields.user_fields import (
    list_user_fields,
    user_partial_fields,
)
from api.services.user_service import UserService

from . import api
from .wraps import WebApiResource


class UsersResource(WebApiResource):
    # 越是基础的，越需要放到最后面，这个是实现依赖

    @manager_required
    @marshal_with(list_user_fields)
    def get(self, user):
        users = UserService.load_users()
        return users


class UserResource(WebApiResource):

    @manager_required
    @marshal_with(user_partial_fields)
    def get(self, user, pk):
        user = UserService.load_user(pk)
        return user


class UserSelfResource(WebApiResource):

    @marshal_with(user_partial_fields)
    def get(self, user):
        return user

    @marshal_with(user_partial_fields)
    def put(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, location="json")
        parser.add_argument("password", type=str, location="json")
        args = parser.parse_args()

        username = args.username
        password = args.password

        return UserService.change_password(
            user,
            username=username,
            password=password,
        )


api.add_resource(UserSelfResource, "/self")

api.add_resource(UsersResource, "/users")
api.add_resource(UserResource, "/users/<pk>")
