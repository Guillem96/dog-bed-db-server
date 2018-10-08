from dbdb_todo.model.json_object import JsonObject
import json

class User(JsonObject):	
	def __init__(self, username, password, email="", tasks=[]):
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
		
		return cls(data["username"], 
					data["password"], 
					data.get("email", ""), 
					data.get("tasks", []))