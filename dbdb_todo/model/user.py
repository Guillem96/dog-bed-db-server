from dbdb_todo.model.json_object import JsonObject
from dbdb_todo.model.task import Task

import json


class User(JsonObject):
    def __init__(self, first_name, last_name, username, password, email="", tasks=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.tasks = tasks

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, task_idx):
        del self.tasks[task_idx]

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        tasks = [Task.from_json(json.dumps(t)) for t in data.get("tasks", [])]
        return cls(data["first_name"],
                   data["last_name"],
                   data["username"],
                   data["password"],
                   data.get("email", ""),
                   tasks)
