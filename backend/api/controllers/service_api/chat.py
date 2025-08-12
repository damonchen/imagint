import logging
import json
import time
import uuid
from urllib.parse import urlencode
from flask import current_app
from flask_restful import marshal_with, reqparse
from flask import stream_with_context

from api.data.fields.task_fields import partial_task_fields
from api.services.chat_service import (
    ChatService,
    ChatMessageService,
    ChatMessageImageService,
)
from api.data.fields.chat import (
    page_chat_fields,
    chat_fields,
    page_chat_message_fields,
    chat_message_fields,
    chat_message_image_fields,
    list_chat_message_fields,
)
from api.libs.sign_url import encrypt_id, sign_url
from api.libs.image_url import ImageURLBuilder

from . import api
from .wraps import WebApiResource

logger = logging.getLogger(__name__)


class ChatsResource(WebApiResource):

    @marshal_with(page_chat_fields)
    def get(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument("page", type=int, location="args", default=1)
        parser.add_argument("per_page", type=int, location="args", default=10)
        args = parser.parse_args()

        page = args.page
        per_page = args.per_page

        chats = ChatService.get_chats_by_page(user, page=page, page_size=per_page)

        return chats

    @marshal_with(chat_fields)
    def post(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument("prompt", type=str, location="json", default="")
        args = parser.parse_args()

        prompt = args.prompt

        return ChatService.create_chat(user, prompt)


class ChatResource(WebApiResource):

    @marshal_with(chat_fields)
    def get(self, user, chat_id):
        chat = ChatService.get_chat(user, chat_id)
        return chat


class CurrentChatResource(WebApiResource):
    @marshal_with(chat_fields)
    def get(self, user):
        chat = ChatService.get_latest_chat(user)
        return chat


class ChatMessagesResource(WebApiResource):

    @marshal_with(chat_message_fields)
    def get(self, user, chat_id):
        parser = reqparse.RequestParser()
        args = parser.parse_args()

        chat_messages = ChatMessageService.get_chat_messages(user, chat_id)
        logger.info("chat messages %s", chat_messages)

        return chat_messages

    @marshal_with(chat_message_fields)
    def post(self, user, chat_id):
        parser = reqparse.RequestParser()
        parser.add_argument("prompt", type=str, location="json", required=True)
        parser.add_argument("params", type=dict, location="json", required=True)
        args = parser.parse_args()

        prompt = args.prompt
        params = args.params
        count = params.get("count", 1)

        chat_message = ChatMessageService.create_messages(
            user, chat_id, prompt, params, count
        )

        return chat_message


class ChatMessageImageResource(WebApiResource):

    @marshal_with(chat_message_image_fields)
    def get(self, user, chat_id, message_id):
        # chat_message = ChatMessageService.get_chat_message(user, chat_id, message_id)

        # aes_key = current_app.config.get('AES_KEY').encode('utf-8')
        # aad = current_app.config.get('AAD').encode('utf-8')
        # sign_key = current_app.config.get('SIGN_KEY').encode('utf-8')
        expire = int(time.time()) + 3600
        # app_web_url = current_app.config.get("APP_WEB_URL")

        builder = ImageURLBuilder()
        images = ChatMessageImageService.get_images(user, message_id)
        prefix = "/image"
        result = []
        for image in images:
            r = image.to_dict()
            urls = builder.build_image_url(prefix, image, expire)
            r.update(urls)
            r["id"] = str(uuid.uuid4())
            result.append(r)

        return result


class ChatMessageResource(WebApiResource):

    @marshal_with(chat_message_fields)
    def get(self, user, chat_id, message_id):
        chat_message = ChatMessageService.get_chat_message(user, chat_id, message_id)
        return chat_message

    @marshal_with(chat_message_fields)
    def post(self, user, chat_id, message_id):
        parser = reqparse.RequestParser()
        parser.add_argument("prompt", type=str, location="json", required=True)
        parser.add_argument("params", type=dict, location="json", required=True)
        args = parser.parse_args()

        prompt = args.prompt
        params = args.params if args.params else {}

        ims = ChatMessageService.create_messages(
            user, chat_id, message_id, prompt, params
        )
        return ims


api.add_resource(ChatsResource, "/chats")
api.add_resource(CurrentChatResource, "/chats/current")
api.add_resource(ChatMessagesResource, "/chats/<chat_id>/messages")
api.add_resource(
    ChatMessageImageResource, "/chats/<chat_id>/messages/<message_id>/images"
)
api.add_resource(ChatMessageResource, "/chats/<chat_id>/messages/<message_id>")
api.add_resource(ChatResource, "/chats/<chat_id>")
