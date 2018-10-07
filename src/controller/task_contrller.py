import json
from flask import request, Response
from model.task import Task

class TaskController(object):
	
	def __init__(self, database, user_ctrl):
		self.database = database
		self.user_controller = user_ctrl

	def store(self, request, username):
		if request.data:
			try:
				body = json.loads(request.data)
				if body["name"] in self.database:
					return Response('{ "msg": "This task name already exists" }', status=400)

				new_task = Task(body["name"], body["description"], body["date_limit"])
				self.user_controller.add_task(username, new_task.name)
				self.database[new_task.name] = new_task.to_json()
				self.database.commit()
				return Response(self.database[new_task.name], status=201)
			except KeyError:
				return Response('{ "msg": "Properties missing" }', status=400)
			except UnicodeDecodeError:
				return Response('{ "msg": "Json body is required" }', status=400)

			
		return Response('{ "msg": "Json body is required" }', status=400)
	
