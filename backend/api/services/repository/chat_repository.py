import logging
from typing import Optional, List
from api.data.models.chat import Chat, ChatMessage, ChatMessageImage
from api.data.models.account import Account
from api.extensions.database import db


class ChatRepository(object):

    @staticmethod
    def create_chat(account: Account, title: str) -> Chat:
        chat = Chat(account_id=account.id, title=title)
        db.session.add(chat)
        db.session.flush()
        return chat

    @staticmethod
    def get_chat(account: Account, chat_id: str) -> Optional[Chat]:
        return Chat.query.filter_by(account_id=account.id).get(chat_id)

    @staticmethod
    def get_chats_by_page(account: Account, page: int, page_size: int):
        return (
            Chat.query.filter_by(account_id=account.id)
            .order_by(Chat.created_at.desc())
            .paginate(page=page, per_page=page_size)
        )

    @staticmethod
    def get_all_chats(account: Account) -> List[Chat]:
        return (
            Chat.query.filter_by(account_id=account.id)
            .order_by(Chat.created_at.desc())
            .all()
        )

    @staticmethod
    def update_chat(account: Account, chat_id: str, title: str) -> Optional[Chat]:
        chat = Chat.query.filter_by(account_id=account.id).get(chat_id)
        if chat:
            chat.title = title
            db.session.add(chat)
            db.session.flush()
        return chat

    @staticmethod
    def delete_chat(account: Account, chat_id: str) -> bool:
        chat = Chat.query.filter_by(account_id=account.id).get(chat_id)
        if chat:
            db.session.delete(chat)
            db.session.flush()
            return True
        return False


class ChatMessageRepository(object):

    @staticmethod
    def create_message(
            account: Account, chat_id: str, prompt: str, params: str
    ) -> ChatMessage:
        message = ChatMessage(
            account_id=account.id,
            chat_id=chat_id,
            prompt=prompt,
            params=params,
            status="pending",
        )
        db.session.add(message)
        db.session.flush()
        return message

    @staticmethod
    def get_chat_messages(account: Account, chat_id: str, page: int, page_size: int):
        return (
            ChatMessage.query.filter_by(account_id=account.id, chat_id=chat_id)
            .order_by(ChatMessage.created_at.desc())
            .paginate(page=page, per_page=page_size)
        )

    @staticmethod
    def get_chat_message(
            account: Account, chat_id: str, message_id: str
    ) -> ChatMessage:
        return ChatMessage.query.filter_by(
            account_id=account.id, chat_id=chat_id, id=message_id
        ).first()

    @staticmethod
    def update_message_translation(
            account: Account,
            message_id: str,
            translated_text: str,
            translated_image_path: str,
    ) -> Optional[ChatMessage]:
        message = ChatMessage.query.filter_by(account_id=account.id).get(message_id)
        if message:
            message.translated_text = translated_text
            message.translated_image_path = translated_image_path

            db.session.add(message)
            db.session.flush()
        return message

    @staticmethod
    def delete_message(account: Account, message_id: str) -> bool:
        message = ChatMessage.query.filter_by(account_id=account.id).get(message_id)
        if message:
            db.session.delete(message)
            db.session.flush()
            return True
        return False


class ChatMessageImageRepository(object):

    @staticmethod
    def create_message_image(account: Account, message: ChatMessage | int, image: str):
        if isinstance(message, ChatMessage):
            message_id = message.id
        else:
            message_id = message

        message_image = ChatMessageImage(
            account_id=account.id, chat_message_id=int(message_id), image_path=image
        )
        db.session.add(message_image)
        db.session.flush()

        return message_image

    @staticmethod
    def get_message_images(account: Account, message: ChatMessage | int):
        if isinstance(message, ChatMessage):
            message_id = message.id
        else:
            message_id = message

        return (
            db.session.query(ChatMessageImage)
            .filter(ChatMessageImage.account_id == account.id)
            .filter(ChatMessageImage.chat_message_id == message.id)
            .all()
        )

    @staticmethod
    def get_image(image_id: int):
        image = db.session.query(ChatMessageImage).get(image_id)
        return image
