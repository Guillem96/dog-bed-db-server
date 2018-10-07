import json
from flask import request, Response
from model.user import User
from model.task import Task

class UserController(object):
	
	def __init__(self, database):
		self.database = database

	def save(self, user):
		self.database[user.username] = user.to_json()
		self.database.commit()

	def store(self, request):
		if request.data:
			try:
				body = json.loads(request.data)
				new_user = User(body["username"], body["password"], body.get("email", ""))
				self.database[new_user.username] = new_user.to_json()
				self.database.commit()
				return Response(self.database[new_user.username], status=201)
			except KeyError:
				return Response(status=400)
			except UnicodeDecodeError:
				return Response('{ "msg": "Json body is required" }', status=400)

		return Response('{ "msg": "Json body is required" }', status=400)
	
	def login(self, request):
		if request.data:
			body = json.loads(request.data)
			try:
				user = json.loads(self.database[body["username"]])
				if user["password"] == body["password"]:
					return Response(status=200)

			except KeyError:
				return Response(status=403)
			except UnicodeDecodeError:
				return Response('{ "msg": "Json body is required" }', status=400)
			
		return Response(status=403)

	def delete(self, username):
		del self.database[username]
		self.database.commit()
	
	def get_password(self, username):
		try:
			return json.loads(self.database[username])["password"]
		except KeyError:
			return None

	def get(self, username):
		try:
			data = self.database[username]
			return Response(data, 200)

		except KeyError:
			return Response(status=404)

	def get_tasks(self, username):
		try:
			data = json.loads(self.database[username])
			tasks = [ t for t in data["tasks"] ]
			return Response(tasks, 200)

		except KeyError:
			return Response(status=404)
	
	def add_task(self, username, task_id):
		try:
			user = User.from_json(self.database[username])
			user.add_task(task_id)
			self.save(user)
			return Response(user.to_json(), 200)

		except KeyError:
			return Response(status=404)
