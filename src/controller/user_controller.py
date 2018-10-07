import json
from flask import request, Response
from model.user import User

class UserController(object):
	
	def __init__(self, database):
		self.database = database

	def store(self, request):
		if request.data:
			try:
				body = json.loads(request.data)
				new_user = User(body["username"], body["password"])
			except KeyError:
				return Response(status=400)
			
			self.database[new_user.username] = new_user.to_json()
			return Response(status=201)

		return Response(status=400)
	
	def login(self, request):
		if request.data:
			body = json.loads(request.data)
			
			try:
				user = json.loads(self.database[body["username"]])

				if user["password"] == body["password"]:
					return Response(status=200)

			except KeyError:
				return Response(status=403)

		return Response(status=403)

	def delete(self, username):
		del self.database[username]
	
	def get(self, username):
		return self.database[username]
