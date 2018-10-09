import json
from flask import request, Response
from dbdb_todo.model.user import User
from dbdb_todo.model.task import Task
from dbdb_todo.controller.controller import Controller


class UserController(Controller):

    def __init__(self, database):
        self.database = database

    def save(self, user):
        self.database[user.username] = user.to_json()
        self.database.commit()

    def _register(self, data, **kwargs):
        if data["username"] == "" or data["password"] == "":
            return Response('{ "msg": "Username and passowrd cannot be blank" }', status=400)

        if data["username"] in self.database:
            return Response('{ "msg": "The username ' + data["username"] + ' already exists" }', status=400)

        new_user = User(data["first_name"], data["last_name"],
                        data["username"], data["password"],
                        data.get("email", ""))
        result = new_user.to_json()
        self.database[new_user.username] = result
        self.database.commit()
        return Response(result, status=201)

    def store(self, request):
        return self.process_request(request, self._register)

    def get_password(self, username):
        try:
            return json.loads(self.database[username])["password"]
        except KeyError:
            return None

    def _identity(self, data, **kwargs):
        if not "username" in kwargs:
            return Response("{ 'msg': 'User not found' }", status=404)

        data = self.database[kwargs.get("username")]
        return Response(data, 200)

    def get(self, request):
        return self.process_request(request, self._identity)
