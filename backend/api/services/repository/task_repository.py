from api.data.models.enums import TaskStatus, TaskWebTokenStatus
from api.extensions.database import db
from api.data.models.task import Task, TaskWebToken
from api.utils.uuid import generate_db_id


class TaskRepository(object):

    @staticmethod
    def create_task(account, payload, status=TaskStatus.PENDING.value):
        """Create a new task"""
        task_id = generate_db_id()
        task = Task(
            account_id=account.id,
            task_id=task_id,
            payload=payload,
            status=status,
            created_by=account.id,
            updated_by=account.id,
        )
        db.session.add(task)
        db.session.flush()

        return task

    @staticmethod
    def load_task_by_id(id):
        """Load task by id"""
        return db.session.query(Task).filter(Task.id == id).first()

    @staticmethod
    def load_task_by_task_id(task_id):
        """Load task by task_id"""
        return db.session.query(Task).filter(Task.task_id == task_id).first()

    @staticmethod
    def list_tasks(account, status=None, page=1, per_page=10):
        """List tasks for account"""
        offset = (page - 1) * per_page
        limit = per_page
        query = db.session.query(Task).filter(Task.account_id == account.id)
        if status is not None:
            query = query.filter(Task.status == status)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return query.all(), query.count()

    @staticmethod
    def update_task(task, account, status, result=None):
        """Update task status and result"""
        task.status = status
        task.updated_by = account.id

        if result is not None:
            task.result = result

        db.session.add(task)
        db.session.flush()

        return task


class TaskWebTokenRepository(object):
    @staticmethod
    def create_task_web_token(task_id, token):
        """Create a new task web token"""
        task_web_token = TaskWebToken(
            token=token,
        )
        db.session.add(task_web_token)
        db.session.flush()
        return task_web_token

    @staticmethod
    def load_task_web_token(token):
        """Load task web token"""
        return (
            db.session.query(TaskWebToken).filter(TaskWebToken.token == token).first()
        )

    @staticmethod
    def delete_task_web_token(token):
        """Delete task web token"""
        db.session.query(TaskWebToken).filter(TaskWebToken.token == token).delete()
        db.session.flush()

    @staticmethod
    def disable_web_token(token):
        """Disable task web token"""
        task_web_token = TaskWebToken.query.filter(TaskWebToken.token == token).first()
        if task_web_token:
            task_web_token.status = TaskWebTokenStatus.DISABLED.value
            db.session.add(task_web_token)
            db.session.flush()
            return task_web_token
        return None
