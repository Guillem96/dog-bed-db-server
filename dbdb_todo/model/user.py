from dbdb_todo.model.json_object import JsonObject
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

        return cls(data["first_name"],
                   data["last_name"],
                   data["username"],
                   data["password"],
                   data.get("email", ""),
                   data.get("tasks", []))
