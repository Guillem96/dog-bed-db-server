import json
from flask import request, Response
from dbdb_todo.model.user import User
from dbdb_todo.model.task import Task
from dbdb_todo.controller.controller import Controller


class TaskController(Controller):

    def __init__(self, database, user_ctrl):
        self.database = database
        self.user_ctrl = user_ctrl

    def add_task(self, request):
        return self.process_request(request, self._add_task)

    def delete_task(self, request, index):
        return self.process_request(request, self._delete, index)

    def update_task(self, request, index):
        return self.process_request(request, self._add_task, index)

    def _add_task(self, data, **kwargs):
        if not isinstance(data["tags"], list):
            return Response("{ 'msg': 'tags must be an array'}", status=400)

        new_task = Task(data["name"], data["description"],
                        data["date_limit"], data.get("done", False), data["tags"])

        user = User.from_json(self.database[kwargs.get("username")])
        status = 201
        index = kwargs.get("index")
        if index < 0:
            user.add_task(new_task)         # Add
        elif index <= len(user.tasks):      # or
            user.tasks[index] = new_task    # Override
            status = 200
        else:
            return Response("{ 'msg': 'Invalid task'}", status=400)

        self.user_ctrl.save(user)

        return Response(user.to_json(), status=status)

    def _delete(self, data, **kwargs):
        user = User.from_json(self.database[kwargs.get("username")])
        user.delete_task(kwargs.get("index"))
        self.user_ctrl.save(user)
        return Response(user.to_json(), 200)
