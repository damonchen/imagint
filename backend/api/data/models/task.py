from datetime import datetime
from sqlalchemy import func
from api.extensions.database import db
from api.data.models.types import JSONType, TimeStamp
from api.utils.uuid import generate_db_id


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String(155), unique=True)  # uuid for tracking task
    # name = db.Column(db.String(255))  # 任务的名称, 用.分隔，前面两个时exchange，后面一个时routing key
    account_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), default="pending")
    payload = db.Column(JSONType, nullable=True)
    result = db.Column(JSONType, nullable=True)
    done_at = db.Column(TimeStamp, nullable=True)
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )


class TaskWebToken(db.Model):
    __tablename__ = "task_web_tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(155), unique=True)
    status = db.Column(db.String(50), default="active")
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(TimeStamp, nullable=False, server_default=func.now())
    updated_by = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(
        TimeStamp,
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def is_not_active(self):
        return not self.is_active
