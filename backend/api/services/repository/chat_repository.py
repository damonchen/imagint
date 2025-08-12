import logging
import time
from collections import defaultdict

from sqlalchemy import desc

from typing import Optional, List
from api.data.models.chat import Chat, ChatMessage, ChatMessageImage
from api.data.models.user import User
from api.extensions.database import db
from api.libs.image_url import ImageURLBuilder


class ChatRepository(object):

    @staticmethod
    def create_chat(user: User, title: str) -> Chat:
        chat = Chat(user_id=user.id, title=title)
        db.session.add(chat)
        db.session.flush()
        return chat

    @staticmethod
    def get_chat(user: User, chat_id: str) -> Optional[Chat]:
        return Chat.query.filter_by(user_id=user.id).get(chat_id)

    @staticmethod
    def get_latest_chat(user: User):
        return (
            Chat.query.filter_by(user_id=user.id)
            .order_by(desc(Chat.created_at))
            .first()
        )

    @staticmethod
    def get_chats_by_page(user: User, page: int, page_size: int):
        return (
            Chat.query.filter_by(user_id=user.id)
            .order_by(Chat.created_at.desc())
            .paginate(page=page, per_page=page_size)
        )

    @staticmethod
    def get_all_chats(user: User) -> List[Chat]:
        return (
            Chat.query.filter_by(user_id=user.id).order_by(Chat.created_at.desc()).all()
        )

    @staticmethod
    def update_chat(user: User, chat_id: str, title: str) -> Optional[Chat]:
        chat = Chat.query.filter_by(user_id=user.id).get(chat_id)
        if chat:
            chat.title = title
            db.session.add(chat)
            db.session.flush()
        return chat

    @staticmethod
    def delete_chat(user: User, chat_id: str) -> bool:
        chat = Chat.query.filter_by(user_id=user.id).get(chat_id)
        if chat:
            db.session.delete(chat)
            db.session.flush()
            return True
        return False


class ChatMessageRepository(object):

    @staticmethod
    def create_message(
        user: User, chat_id: str, prompt: str, params: str, count: int = 1
    ) -> ChatMessage:
        message = ChatMessage(
            user_id=user.id,
            chat_id=chat_id,
            prompt=prompt,
            params=params,
            status="pending",
            count=count,
        )
        db.session.add(message)
        db.session.flush()
        return message

    @staticmethod
    def get_chat_message_pagination(
        user: User, chat_id: str, page: int, page_size: int
    ):
        return (
            ChatMessage.query.filter_by(user_id=user.id, chat_id=chat_id)
            .order_by(ChatMessage.created_at.desc())
            .paginate(page=page, per_page=page_size)
        )

    @staticmethod
    def get_chat_messages(user: User, chat_id: str):
        messages = (
            ChatMessage.query.filter_by(user_id=user.id, chat_id=chat_id).order_by(
                ChatMessage.created_at
            )
        ).all()
        return messages

    @staticmethod
    def get_chat_message(user: User, chat_id: str, message_id: str) -> ChatMessage:
        return ChatMessage.query.filter_by(
            user_id=user.id, chat_id=chat_id, id=message_id
        ).first()

    @staticmethod
    def update_message_translation(
        user: User,
        message_id: str,
        translated_text: str,
        translated_image_path: str,
    ) -> Optional[ChatMessage]:
        message = ChatMessage.query.filter_by(user_id=user.id).get(message_id)
        if message:
            message.translated_text = translated_text
            message.translated_image_path = translated_image_path

            db.session.add(message)
            db.session.flush()
        return message

    @staticmethod
    def delete_message(user: User, message_id: int) -> bool:
        message = ChatMessage.query.filter_by(user_id=user.id).get(message_id)
        if message:
            db.session.delete(message)
            db.session.flush()
            return True
        return False

    @staticmethod
    def update_message_status(user: User, message_id: int, status: str):
        message = db.session.query(ChatMessage).get(message_id)
        if message is None:
            return None

        message.status = status
        message.updated_by = user.id

        db.session.add(message)
        db.session.flush()

        return message


class ChatMessageImageRepository(object):

    @staticmethod
    def create_message_image(user: User, message: ChatMessage | int, image: str):
        if isinstance(message, ChatMessage):
            message_id = message.id
        else:
            message_id = message

        message_image = ChatMessageImage(
            user_id=user.id,
            chat_message_id=int(message_id),
            image_path=image,
        )
        db.session.add(message_image)
        db.session.flush()

        return message_image

    @staticmethod
    def get_message_images(user: User, message: ChatMessage | int):
        if isinstance(message, ChatMessage):
            message_id = message.id
        else:
            message_id = message

        return (
            db.session.query(ChatMessageImage)
            .filter(ChatMessageImage.user_id == user.id)
            .filter(ChatMessageImage.chat_message_id == message_id)
            .all()
        )

    @staticmethod
    def get_images_by_message_ids(message_ids):
        message_images = (
            db.session.query(ChatMessageImage)
            .filter(ChatMessageImage.chat_message_id.in_(message_ids))
            .all()
        )
        return message_images

    @staticmethod
    def get_image(image_id: int):
        image = db.session.query(ChatMessageImage).get(image_id)
        return image
