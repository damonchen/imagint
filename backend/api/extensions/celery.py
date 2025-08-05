from datetime import timedelta
from celery import Celery, Task
import logging

logger = logging.getLogger(__name__)


class CeleryProxy:
    def __init__(self, app=None):
        self._celery = None
        self._app = None

        if app is not None:
            self.init_app(app)

    def task(self, *args, **kwargs):
        def decorator(func):
            if self._celery is None:
                # Store the decorator arguments for later use
                func._celery_args = args
                func._celery_kwargs = kwargs
                return func
            return self._celery.task(*args, **kwargs)(func)

        return decorator

    def __getattr__(self, name):
        if self._celery is None:
            raise RuntimeError("Celery extension is not initialized")
        return getattr(self._celery, name)

    def init_app(self, app):
        self._app = app

        def CeleryTask(Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(self, *args, **kwargs)

        try:
            celery_app = Celery(
                app.name,
                # task_cls = CeleryTask,
                broker=app.config["CELERY_BROKER_URL"],
                backend=app.config["CELERY_BACKEND"],
                task_ignore_result=True,
            )

            celery_app.conf.update(
                result_backend=app.config["CELERY_RESULT_BACKEND"],
                broker_connection_retry_on_startup=True,
                worker_prefetch_multiplier=1,  # 防止worker预取过多任务
                task_acks_late=True,  # 任务完成后才确认
                worker_max_tasks_per_child=1000,  # 每个worker处理1000个任务后重启
            )

            # Remove SSL options to the Celery configuration
            ssl_options = {
                "ssl_cert_reqs": None,
                "ssl_ca_certs": None,
                "ssl_certfile": None,
                "ssl_keyfile": None,
            }
            if app.config["BROKER_USE_SSL"]:
                celery_app.conf.update(
                    broker_use_ssl=ssl_options,  # Add the SSL options to the broker configuration
                )

            celery_app.set_default()
            app.extensions["celery"] = celery_app

            imports = [
                "schedule.clean_embedding_cache_task",
                "schedule.clean_unused_datasets_task",
            ]

            beat_schedule = {
                "clean_embedding_cache_task": {
                    "task": "schedule.clean_embedding_cache_task.clean_embedding_cache_task",
                    "schedule": timedelta(days=1),
                },
                "clean_unused_datasets_task": {
                    "task": "schedule.clean_unused_datasets_task.clean_unused_datasets_task",
                    "schedule": timedelta(days=1),
                },
            }
            celery_app.conf.update(beat_schedule=beat_schedule, imports=imports)

            self._celery = celery_app
            logger.info("Celery扩展初始化成功")

        except Exception as e:
            logger.error(f"Celery扩展初始化失败: {e}")
            raise

    def shutdown(self):
        """关闭Celery连接"""
        if self._celery is not None:
            try:
                # 关闭broker连接
                if hasattr(self._celery, "connection"):
                    self._celery.connection.close()

                # 关闭backend连接
                if hasattr(self._celery, "backend") and self._celery.backend:
                    self._celery.backend.close()

                logger.info("Celery连接已关闭")
            except Exception as e:
                logger.error(f"关闭Celery连接时出错: {e}")

    def get_celery_app(self):
        """获取Celery应用实例"""
        return self._celery


celery_app = CeleryProxy()


def init_app(app):
    celery_app.init_app(app)
