import logging
from flask_restful import marshal_with, reqparse
from flask import stream_with_context

from api.data.fields.task_fields import partial_task_fields
from api.services.chat_service import ChatService
from api.data.fields.chat import (
    page_chat_fields,
    chat_fields,
    page_chat_message_fields,
    chat_message_fields,
)
from . import api
from .wraps import WebApiResource


class ChatsResource(WebApiResource):

    @marshal_with(page_chat_fields)
    def get(self, account):
        parser = reqparse.RequestParser()
        parser.add_argument("page", type=int, location="args", default=1)
        parser.add_argument("per_page", type=int, location="args", default=10)
        args = parser.parse_args()

        page = args.page
        per_page = args.per_page

        chats = ChatService.get_chats_by_page(account, page=page, page_size=per_page)

        return chats

    @marshal_with(chat_fields)
    def post(self, account):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=int, location="json", default="")
        args = parser.parse_args()

        title = args.title

        return ChatService.create_chat(account, title)


class ChatResource(WebApiResource):

    @marshal_with(chat_fields)
    def get(self, account, chat_id):
        chat = ChatService.get_chat(account, chat_id)
        return chat


class ChatMessagesResource(WebApiResource):

    @marshal_with(page_chat_message_fields)
    def get(self, account, chat_id):
        parser = reqparse.RequestParser()
        parser.add_argument("page", type=int, location="args", default=1)
        parser.add_argument("per_page", type=int, location="args", default=10)
        args = parser.parse_args()

        page = args.page
        per_page = args.per_page

        chat_messages = ChatService.get_chat_messages(account, chat_id, page, per_page)

        return chat_messages


class ChatTranslateResource(WebApiResource):

    @marshal_with(partial_task_fields)
    def post(self, account, chat_id):
        parser = reqparse.RequestParser()
        parser.add_argument("files", type=list, location="json", default=None)
        args = parser.parse_args()

        files = args.files
        if files:
            print("args files", files)
            task = ChatService.translate_message(account, chat_id, files)
            return task


class ChatMessageStreamResource(WebApiResource):

    def get(self, account, chat_id):
        # using yield for stream info response
        def generate():
            yield "hello world"

        return stream_with_context(generate())


class ChatMessageResource(WebApiResource):

    @marshal_with(chat_message_fields)
    def get(self, account, chat_id, message_id):
        chat_message = ChatService.get_chat_message(account, chat_id, message_id)
        return chat_message


api.add_resource(ChatsResource, "/chats")
api.add_resource(ChatMessagesResource, "/chats/<chat_id>/messages")
api.add_resource(ChatTranslateResource, "/chats/<chat_id>/translate")
api.add_resource(ChatMessageStreamResource, "/chats/<chat_id>/messages/stream")
api.add_resource(ChatMessageResource, "/chats/<chat_id>/messages/<message_id>")
api.add_resource(ChatResource, "/chats/<chat_id>")
