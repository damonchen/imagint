import uuid
import logging
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Index, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from api.extensions.database import db

from api.data.models.types import JSONType


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = Column(String(512), nullable=False)
    account_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    __table_args__ = (Index("uix_chat", "chat_id"),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(64), nullable=False)
    account_id = Column(Integer, nullable=False)
    type = Column(String(32), default="text")  # text, image, etc.
    prompt = Column(Text)  # image path，储存的是attachment中的file_id的列表？
    params = Column(JSONType)  # 其他参数
    status = Column(String(32), default="pending")  # pending, running, success, failed
    image_path = Column(Text, nullable=True)  # 如果是图片消息，存储图片路径
    count = Column(Integer, default=1)  # 图像的数量或者视频的数量
    created_at = Column(DateTime, default=datetime.now)

    @property
    def image_count(self):
        return self.count


class ChatMessageImage(db.Model):
    __tablename__ = "chat_message_images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, nullable=False)
    chat_message_id = Column(db.Integer, ForeignKey("chat_messages.id"), nullable=False)
    image_path = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # chat_message = relationship("ChatMessage", back_populates="images")

    def to_dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "chat_message_id": self.chat_message_id,
        }