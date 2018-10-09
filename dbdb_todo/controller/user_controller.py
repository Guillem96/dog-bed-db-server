import json
from flask import request, Response
from dbdb_todo.model.user import User
from dbdb_todo.model.task import Task


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

                if body["username"] == "" or body["password"] == "":
                    return Response('{ "msg": "Username and passowrd cannot be blank" }', status=400)

                if body["username"] in self.database:
                    return Response('{ "msg": "The username ' + body["username"] + ' already exists" }', status=400)

                new_user = User(body["first_name"], body["last_name"],
                                body["username"], body["password"],
                                body.get("email", ""))
                self.database[new_user.username] = new_user.to_json()
                self.database.commit()
                print new_user.to_json()
                return Response(new_user.to_json(), status=201)
            except KeyError:
                return Response('{ "msg": "Missing properties" }', status=400)
            except (UnicodeDecodeError, ValueError):
                return Response('{ "msg": "Json body is incorrect" }', status=400)

        return Response('{ "msg": "Json body is required" }', status=400)

    def login(self, request):
        if request.data:
            body = json.loads(request.data)
            try:
                user = json.loads(self.database[body["username"]])
                if user["password"] == body["password"]:
                    return Response(status=200)

            except KeyError:
                return Response("{ 'msg': 'Missing properties' }", status=403)
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

    def get(self, request):
        try:
            username = request.authorization.get("username")
            data = self.database[username]
            data = json.loads(data)
            del data["password"]
            data = json.dumps(data)
            return Response(data, 200)

        except KeyError as err:
            return Response("{ 'msg': '" + str(err) + "'}", status=404)

    def add_task(self, request):
        username = request.authorization.get("username")
        if request.data:
            try:
                return Response(self._add_task(username, json.loads(request.data)).to_json(), 201)
            except KeyError:
                return Response('{ "msg": "Properties missing" }', status=400)
            except UnicodeDecodeError:
                return Response('{ "msg": "Json body is required" }', status=400)

        return Response('{ "msg": "Json body is required" }', status=400)

    def delete_task(self, request, index):
        username = request.authorization.get("username")
        if not username:
            return Response(status=403)
        try:
            return Response(self._delete_task(username, index).to_json(), 200)
        except KeyError:
            return Response('{ "msg": "User not found" }', status=400)

    def update_task(self, request, index):
        username = request.authorization.get("username")
        if not username:
            return Response(status=403)
        try:
            user = self._delete_task(username, index)
            user = self._add_task(username, json.loads(request.data), index)
            if not user:
                return Response("{ 'msg': 'Invalid index' }", 400)
            return Response(user.to_json(), 200)
        except KeyError:
            return Response('{ "msg": "User not found" }', status=400)

    def _add_task(self, username, task, index=-1):
        new_task = Task(task["name"], task["description"], task["date_limit"])
        user = User.from_json(self.database[username])
        if index < 0:
            user.add_task(new_task)
        elif index <= len(user.tasks):
            user.tasks[index] = new_task
        else:
            return None

        self.save(user)
        return user

    def _delete_task(self, username, index):
        user = User.from_json(self.database[username])
        user.delete_task(index)
        self.save(user)
        return user
