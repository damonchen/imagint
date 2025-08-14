import json
import logging
import uuid
from collections import defaultdict
import time

from flask_sqlalchemy.pagination import Pagination
from typing import List

from .repository.task_repository import TaskRepository
from .task_service import TaskService
from .redis_service import RedisService
from .credit_service import CreditService
from api.extensions.database import transaction
from .repository.attachment_repository import AttachmentRepository
from .repository.chat_repository import (
    ChatRepository,
    ChatMessageRepository,
    ChatMessageImageRepository,
)
from api.data.models.chat import Chat, ChatMessage
from api.data.models.user import User
from api.libs.url import get_file_url
from api.libs.image_url import ImageURLBuilder

logger = logging.getLogger(__name__)


def get_title_from_prompt(propmt):
    return propmt[:500]


class ChatService(object):

    @staticmethod
    def create_chat(user: User, prompt: str) -> Chat:
        # get title from propmt
        title = get_title_from_prompt(prompt)
        return ChatRepository.create_chat(user, title)

    @staticmethod
    def get_chat(user: User, chat_id: str) -> Chat:
        return ChatRepository.get_chat(user, chat_id)

    @staticmethod
    def get_latest_chat(user: User):
        return ChatRepository.get_latest_chat(user)

    @staticmethod
    def get_chats_by_page(user: User, page: int, page_size: int) -> Pagination:
        return ChatRepository.get_chats_by_page(user, page, page_size)

    @staticmethod
    def get_all_chats(user: User) -> List[Chat]:
        return ChatRepository.get_all_chats(user)

    @staticmethod
    def update_chat(user: User, chat_id: str, title: str) -> Chat:
        return ChatRepository.update_chat(user, chat_id, title)

    @staticmethod
    def delete_chat(user: User, chat_id: str) -> bool:
        return ChatRepository.delete_chat(user, chat_id)


class ChatMessageService(object):
    @staticmethod
    def create_messages(
        user: User,
        chat_id: str,
        prompt: str,
        params: dict,
        count: int,
    ) -> ChatMessage:
        # 检查用户是否有足够的credit生成图片
        if not CreditService.check_user_can_generate_image(user, count):
            raise ValueError(
                f"Insufficient credits. You need {count * 4} credits to generate {count} images."
            )

        # 消费credit
        if not CreditService.consume_credits_for_image_generation(user, count):
            raise ValueError("Failed to consume credits. Please try again.")

        message = ChatMessageRepository.create_message(
            user, chat_id, prompt, params, count
        )

        model = params.pop("model", "qwen-image")
        type = params.pop("type")

        # create a task to save the chat message task
        payload = {
            "model": model,
            "type": type,
            "chat_id": chat_id,
            "message_id": message.id,
            "prompt": prompt,
            "params": params,
        }

        task = TaskService.create_task(user, payload)
        # send task info to the backend service to generate image
        RedisService.rpush(
            f"task:{model}:image",
            json.dumps(
                {
                    "task_id": task.task_id,
                }
            ),
        )

        return message

    @staticmethod
    def get_chat_messages(user: User, chat_id: str):
        messages = ChatMessageRepository.get_chat_messages(user, chat_id)

        message_ids = [message.id for message in messages]
        message_images = ChatMessageImageService.get_images_by_message_ids(message_ids)

        message_image_map = defaultdict(list)
        for image in message_images:
            message_image_map[image.chat_message_id].append(image)

        prefix = "/image"
        builder = ImageURLBuilder()
        expire = int(time.time()) + 3600
        newMessages = []
        for message in messages:
            images = message_image_map[message.id]

            new_images = []
            for image in images:
                urls = builder.build_image_url(prefix, image, expire)
                item = image.to_dict()
                item["id"] = str(uuid.uuid4())
                item.update(urls)
                new_images.append(item)

            message.images = new_images
            newMessages.append(message)
        return newMessages

    @staticmethod
    def get_chat_message(user: User, chat_id: str, message_id: str) -> ChatMessage:
        message = ChatMessageRepository.get_chat_message(user, chat_id, message_id)

        if message and message.status == "success":
            # 获取该消息的图片
            images = ChatMessageImageService.get_images(user, message_id)

            # 构建图片URL
            prefix = "/image"
            builder = ImageURLBuilder()
            expire = int(time.time()) + 3600

            new_images = []
            for image in images:
                urls = builder.build_image_url(prefix, image, expire)
                item = image.to_dict()
                item["id"] = str(uuid.uuid4())
                item.update(urls)
                new_images.append(item)

            # 将图片数据添加到消息对象
            message.images = new_images

        return message

    @staticmethod
    def delete_message(user: User, message_id: int) -> bool:
        return ChatMessageRepository.delete_message(user, message_id)

    @staticmethod
    def update_message_status(user: User, message_id: int, status: str):
        return ChatMessageRepository.update_message_status(user, message_id, status)


class ChatMessageImageService(object):

    @staticmethod
    @transaction
    def create_images(user, message_id, images):
        ims = []
        for image in images:
            im = ChatMessageImageRepository.create_message_image(
                user, message_id, image
            )
            ims.append(im)

        return ims

    @staticmethod
    def get_images_by_message_ids(message_ids):
        return ChatMessageImageRepository.get_images_by_message_ids(message_ids)

    @staticmethod
    def get_images(user, message_id):
        return ChatMessageImageRepository.get_message_images(user, message_id)

    @staticmethod
    def get_image(image_id):
        return ChatMessageImageRepository.get_image(image_id)
