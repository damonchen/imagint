import json
import logging
from flask_sqlalchemy.pagination import Pagination
from typing import List

from .repository.task_repository import TaskRepository
from .task_service import TaskService
from api.extensions.database import transaction
from .repository.attachment_repository import AttachmentRepository
from .repository.chat_repository import ChatRepository
from api.data.models.chat import Chat, ChatMessage
from api.data.models.account import Account
from api.libs.url import get_file_url

logger = logging.getLogger(__name__)


class ChatService(object):

    @staticmethod
    def create_chat(account: Account, title: str) -> Chat:
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
        account: Account, chat_id: str, prompty: str, params: dict
    ) -> ChatMessage:

        params_str = json.dumps(params) if params else "{}"

        message = ChatMessageRepository.create_message(
            account, chat_id, prompty, params_str
        )
        # push the message to the backend service to generate image

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
    def update_message_translation(
        account: Account,
        message_id: str,
        translated_text: str,
        translated_image_path: str,
    ) -> ChatMessage:
        return ChatMessageRepository.update_message_translation(
            account, message_id, translated_text, translated_image_path
        )

    @staticmethod
    def delete_message(account: Account, message_id: str) -> bool:
        return ChatMessageRepository.delete_message(account, message_id)

    @staticmethod
    @transaction
    def translate_message(account: Account, chat_id: str, files: List):
        file_ids = [file["file_id"] for file in files]
        image_path_ids = json.dumps(file_ids)
        message = ChatMessageRepository.create_message(
            account, chat_id, image_path_ids=image_path_ids
        )

        image_urls = [get_file_url(file_id) for file_id in file_ids]

        images = dict(zip(file_ids, image_urls))

        payload = {
            "message": {
                "chat_id": message.chat_id,
                "account_id": message.account_id,
                "images": images,
                # 'image_path_ids': file_ids,
                # 'image_urls': image_urls,
            },
        }
        logger.info("translate message payload is %s", payload)
        task = TaskService.create_task_and_dispatch(account, payload)

        return task
