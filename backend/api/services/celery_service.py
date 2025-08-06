import logging
from api.extensions.celery import celery_app


logger = logging.getLogger(__name__)


class CeleryService(object):
    @staticmethod
    def send_task(task_name: str, args: tuple = None, kwargs: dict = None) -> str:
        """
        Send task to Celery worker
        Args:
            task_name: Name of the task
            args: Positional arguments for the task
            kwargs: Keyword arguments for the task
        Returns:
            Task ID
        """
        try:
            task = celery_app.send_task(task_name, args=args or (), kwargs=kwargs or {})
            return task.id
        except Exception as e:
            logger.error(f"Failed to send Celery task: {e}")
            raise

    @staticmethod
    def get_task_result(task_id: str):
        """
        Get task result from Celery
        Args:
            task_id: ID of the task
        Returns:
            Task result
        """
        try:
            result = celery_app.AsyncResult(task_id)
            return {"status": result.status, "result": result.result}
        except Exception as e:
            logger.error(f"Failed to get Celery task result: {e}")
            raise


@celery_app.task
def send_register_token_mail(account, token):
    from api.services.mail_service import MailService

    MailService.send_register_token_mail(account, token)

@celery_app
def create_chat_message(chat_id, message_id, prompt, params):

    # 开启进程，调用worker的model，执行对应的内容
    from api.services.task_service import TaskService

    images = TaskService.create_chat_images(chat_id, message_id, prompt, params)
    # send message to our api service
