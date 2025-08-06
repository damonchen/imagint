import uuid
import logging
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Index, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from api.extensions.database import db


class Chat(db.Model):
    __tablename__ = "chats"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(512), nullable=False)
    account_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    __table_args__ = (Index("uix_chat", "chat_id"),)

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    chat_id = Column(String(64), nullable=False)
    account_id = Column(Integer, nullable=False)
    type = Column(String(32), default="text")  # text, image, etc.
    prompt = Column(Text)  # image path，储存的是attachment中的file_id的列表？
    params = Column(Text)  # 其他参数
    image_path = Column(Text, nullable=True)  # 如果是图片消息，存储图片路径
    created_at = Column(DateTime, default=datetime.now)


class ChatMessageImage(db.Model):
    __tablename__ = "chat_message_images"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = Column(Integer, nullable=False)
    chat_message_id = Column(String(64), ForeignKey("chat_messages.id"), nullable=False)
    image_path = Column(Text, nullable=True)

    chat_message = relationship("ChatMessage", back_populates="images")
