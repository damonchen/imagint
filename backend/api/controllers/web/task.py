import logging
from flask_restful import marshal_with, reqparse
from .errors import NotFoundError
from api.data.fields.task_fields import task_fields, task_pagination_fields
from api.services.task_service import TaskService
from . import api
from .wraps import WebApiResource


class TasksResource(WebApiResource):

    @marshal_with(task_pagination_fields)
    def get(self, account):
        parser = reqparse.RequestParser()
        parser.add_argument("status", type=str, location="args")
        parser.add_argument("page", type=int, location="args", default=1)
        parser.add_argument("per_page", type=int, location="args", default=10)
        args = parser.parse_args()

        status = args.status
        page = args.page
        per_page = args.per_page
        tasks, total = TaskService.list_tasks(
            account, status=status, page=page, per_page=per_page
        )

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "hasMore": total > page * per_page,
            "items": tasks,
        }

    @marshal_with(task_fields)
    def post(self, account):
        parser = reqparse.RequestParser()
        parser.add_argument("payload", type=dict, location="json", required=True)
        args = parser.parse_args()

        payload = args.payload
        task = TaskService.create_task_and_dispatch(account, payload)
        return task


class TaskResource(WebApiResource):

    @marshal_with(task_fields)
    def get(self, account, task_id):
        task = TaskService.get_task(task_id)
        if task is None or task.account_id != account.id:
            raise NotFoundError()
        return task

    @marshal_with(task_fields)
    def put(self, account, task_id):
        parser = reqparse.RequestParser()
        parser.add_argument("status", type=str, location="json", required=True)
        parser.add_argument("result", type=dict, location="json")
        args = parser.parse_args()

        status = args.status
        result = args.result

        task = TaskService.update_task_status(account, task_id, status, result)
        return task


api.add_resource(TasksResource, "/tasks")
api.add_resource(TaskResource, "/tasks/<task_id>")
