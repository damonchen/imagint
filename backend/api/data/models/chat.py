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
    image_path_ids = Column(Text)  # image path，储存的是attachment中的file_id的列表？
    translated_image_path_ids = Column(Text)  # 也是ids
    translated_text = Column(Text)  # 用file_id+翻译内容作为message的信息
    created_at = Column(DateTime, default=datetime.now)
