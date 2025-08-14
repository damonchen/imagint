import logging
import json
from flask_restful import marshal_with, reqparse

from api.services.redis_service import RedisService

from api.services.user_service import UserService
from api.data.fields.task_fields import (
    task_fields,
    task_pagination_fields,
    dispatch_task_fields,
)
from api.services.task_service import TaskService
from api.services.chat_service import ChatMessageImageService, ChatMessageService
from api.services.repository.task_repository import TaskRepository
from . import api
from .wraps import WebApiResource, TaskApiResource
from api.libs.decorator import unified_response
from api.libs.response import make_response


logger = logging.getLogger(__name__)


class TasksResource(WebApiResource):

    @unified_response(task_pagination_fields)
    def get(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument("status", type=str, location="args")
        parser.add_argument("page", type=int, location="args", default=1)
        parser.add_argument("per_page", type=int, location="args", default=10)
        args = parser.parse_args()

        status = args.status
        page = args.page
        per_page = args.per_page
        tasks, total = TaskService.list_tasks(
            user, status=status, page=page, per_page=per_page
        )

        return make_response(
            {
                "page": page,
                "per_page": per_page,
                "total": total,
                "hasMore": total > page * per_page,
                "items": tasks,
            }
        )

    @unified_response(task_fields)
    def post(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument("payload", type=dict, location="json", required=True)
        args = parser.parse_args()

        payload = args.payload
        task = TaskService.create_task_and_dispatch(user, payload)
        return make_response(task)


class TaskResource(TaskApiResource):

    @unified_response(dispatch_task_fields)
    def post(self):
        # 请求获取任务
        parser = reqparse.RequestParser()
        parser.add_argument("task_type", type=str, location="json", required=True)
        parser.add_argument("media_type", type=str, location="json", required=False)
        args = parser.parse_args()
        task_type = args.task_type
        media_type = args.media_type

        key = f"task:{task_type}:{media_type}"
        logger.info("task type key %s", key)

        # get task from redis
        item = RedisService.lpop(key)
        if not item:
            # no task
            return make_response({"task_id": None})

        item = json.loads(item)
        task_id = item["task_id"]
        logger.info("task id is %s", task_id)

        task = TaskService.get_task(task_id)
        if task is None:
            logger.info(f"task {task_id} not found ")
            return make_response({"task_id": None})

        user = UserService.load_user(task.user_id)

        status = "running"
        TaskService.update_task_status(user, task.task_id, status=status)

        # 同时也需要更新chat_messages，表明任务已经在执行中了
        message_id = task.payload.get("message_id")
        ChatMessageService.update_message_status(user, message_id, status=status)

        if task:
            payload = task.payload
            return make_response(
                {
                    "task_id": task_id,
                    "prompt": payload["prompt"],
                    "params": payload["params"],
                    "model": payload.get("model"),
                    "type": payload.get("type"),
                }
            )
        else:
            return make_response({"task_id": None})


class TaskCompleteResource(TaskApiResource):

    @unified_response(task_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("task_id", type=str, location="json", required=True)
        parser.add_argument("status", type=str, location="json", required=True)
        parser.add_argument("result", type=dict, location="json")
        args = parser.parse_args()

        task_id = args.task_id
        status = args.status
        result = args.result

        logger.info("task %s complete %s %s", task_id, status, result)

        task = TaskRepository.load_task_by_task_id(task_id)
        if task is None:
            logger.info(f"task not valid {task_id}")
            return make_response({"task_id": None})

        user = UserService.load_user(task.user_id)
        payload = task.payload

        media_type = result.get("media_type")
        if media_type == "image":
            images = result.get("images")
            message_id = payload.get("message_id")

            ChatMessageImageService.create_images(user, message_id, images)

        task = TaskService.update_task_status(user, task_id, status, result)

        TaskService.update_task_status(user, task_id, status=status)

        message_id = task.payload.get("message_id")
        ChatMessageService.update_message_status(user, message_id, status=status)

        return make_response(task)


api.add_resource(TasksResource, "/tasks")
api.add_resource(TaskResource, "/task")
api.add_resource(TaskCompleteResource, "/task/complete")
