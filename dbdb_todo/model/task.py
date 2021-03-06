from dbdb_todo.model.json_object import JsonObject
import json
import hashlib


class Task(JsonObject):
    def __init__(self, name, description, date_limit, done=False, tags=[]):
        self.name = name
        self.description = description
        self.date_limit = date_limit
        self.done = done
        self.tags = tags

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)

        return cls(data["name"],
                   data["description"],
                   data["date_limit"],
                   data.get("done", False),
                   data["tags"])
