import json
import logging
from flask_sqlalchemy.pagination import Pagination
from typing import List

from .repository.task_repository import TaskRepository
from .task_service import TaskService
from .redis_service import RedisService
from api.extensions.database import transaction
from .repository.attachment_repository import AttachmentRepository
from .repository.chat_repository import (
    ChatRepository,
    ChatMessageRepository,
    ChatMessageImageRepository,
)
from api.data.models.chat import Chat, ChatMessage
from api.data.models.account import Account
from api.libs.url import get_file_url

logger = logging.getLogger(__name__)


def get_title_from_prompt(propmt):
    return propmt


class ChatService(object):

    @staticmethod
    def create_chat(account: Account, prompt: str) -> Chat:
        # get title from propmt
        title = get_title_from_prompt(prompt)
        return ChatRepository.create_chat(account, title)

    @staticmethod
    def get_chat(account: Account, chat_id: str) -> Chat:
        return ChatRepository.get_chat(account, chat_id)

    @staticmethod
    def get_chats_by_page(account: Account, page: int, page_size: int) -> Pagination:
        return ChatRepository.get_chats_by_page(account, page, page_size)

    @staticmethod
    def get_all_chats(account: Account) -> List[Chat]:
        return ChatRepository.get_all_chats(account)

    @staticmethod
    def update_chat(account: Account, chat_id: str, title: str) -> Chat:
        return ChatRepository.update_chat(account, chat_id, title)

    @staticmethod
    def delete_chat(account: Account, chat_id: str) -> bool:
        return ChatRepository.delete_chat(account, chat_id)


class ChatMessageService(object):
    @staticmethod
    def create_messages(
        account: Account, chat_id: str, prompt: str, params: dict
    ) -> ChatMessage:

        params_str = json.dumps(params) if params else "{}"

        message = ChatMessageRepository.create_message(
            account, chat_id, prompt, params_str
        )

        model = params.get("model")

        # create a task to save the chat message task
        payload = {
            "model": model,
            "task_type": model,
            "chat_id": chat_id,
            "message_id": message.id,
            "prompt": prompt,
            "params": params,
        }

        task = TaskService.create_task(account, payload)
        # send task info to the backend service to generate image
        RedisService.rpush(f"task:{model}:image", task.task_id)

        return message

    @staticmethod
    def get_chat_messages(
        account: Account, chat_id: str, page: int, page_size: int
    ) -> Pagination:
        return ChatMessageRepository.get_chat_messages(
            account, chat_id, page, page_size
        )

    @staticmethod
    def get_chat_message(
        account: Account, chat_id: str, message_id: str
    ) -> ChatMessage:
        return ChatMessageRepository.get_chat_message(account, chat_id, message_id)

    @staticmethod
    def delete_message(account: Account, message_id: str) -> bool:
        return ChatMessageRepository.delete_message(account, message_id)


class ChatMessageImageService(object):

    @staticmethod
    @transaction
    def create_images(account, message_id, images):
        ims = []
        for image in images:
            im = ChatMessageImageRepository.create_message_image(
                account, message_id, image
            )
            ims.append(im)

        return ims

    @staticmethod
    def get_images(account, message_id):
        return ChatMessageImageRepository.get_message_images(account, message_id)
