import json
import logging
from api.data.models.enums import TaskStatus
from api.services.errors.common import NotFoundError
from api.services.repository.task_repository import TaskRepository
from api.services.repository.account_repository import AccountRepository
from api.services.rabbitmq_service import RabbitMQService
from api.extensions.database import transaction

logger = logging.getLogger(__name__)


class TaskService(object):

    @staticmethod
    @transaction
    def create_task_and_dispatch(account, payload):
        """Create a new task and dispatch to target exchange and key"""
        # Create task record in database
        task = TaskRepository.create_task(
            account=account,
            payload=payload,
            status=TaskStatus.PENDING.value,
        )

        if not task:
            raise NotFoundError("Failed to create task")

        task_message = {
            "task_id": task.task_id,
            "payload": payload,
        }

        logger.info("push task message to the queue %s", task_message)

        RabbitMQService.publish_task(
            payload=task_message,
        )

        return task

    @staticmethod
    def task_callback(payload: str):
        """Callback from worker to update task status"""
        payload = json.loads(payload)

        task_id = payload["task_id"]
        status = payload["status"]
        result = payload["result"]
        account_id = payload["account_id"]

        account = AccountRepository.load_account(account_id)
        return TaskService.update_task_status(account, task_id, status, result)

    @staticmethod
    @transaction
    def update_task_status(account, task_id, status, result=None):
        """Update task status and result"""
        task = TaskRepository.load_task_by_task_id(task_id)
        if not task:
            raise NotFoundError("Task not found")

        return TaskRepository.update_task(
            task=task, account=account, status=status, result=result
        )

    @staticmethod
    def get_task(task_id):
        """Get task by id"""
        task = TaskRepository.load_task_by_task_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
        return task

    @staticmethod
    def list_tasks(account, status=None, page=1, per_page=10):
        """List tasks for account"""
        return TaskRepository.list_tasks(
            account=account, status=status, page=page, per_page=per_page
        )

    @staticmethod
    @transaction
    def callback_task(task_id, status, result=None):
        """Callback from worker to update task status"""
        task = TaskRepository.load_task_by_task_id(task_id)
        if not task:
            raise NotFoundError("Task not found")

        return TaskRepository.update_task(task=task, status=status, result=result)

    @staticmethod
    @transaction
    def cancel_task(account, task_id):
        """Cancel a pending task"""
        task = TaskRepository.load_task_by_task_id(task_id)
        if not task:
            raise NotFoundError("Task not found")

        if task.status != TaskStatus.PENDING.value:
            raise NotFoundError("Task is not in pending status")

        return TaskRepository.update_task(
            task=task, account=account, status=TaskStatus.CANCELLED.value
        )
