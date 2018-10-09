import os
import tempfile
import json
import base64

import pytest

from dbdb_todo import create_app


@pytest.fixture
def app():
    fd, path = tempfile.mkstemp()
    app = create_app({
        "DATABASE": path,
        "TESTING": True
    })

    yield app

    os.close(fd)
    os.unlink(path)


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions(object):
    headers = {"Content-Type": "application/json"}

    def __init__(self, client):
        self._client = client

    def login(self, username, password):
        headers = self.get_basic_auth(username, password)
        return self._client.post("/login", data="{}", headers=headers)

    def sign_up(self, first_name, last_name, username, password, email):
        data = dict(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )
        return self._client.post("/sign-up", data=json.dumps(data), headers=AuthActions.headers)

    def identity(self, username, password):
        return self._client.get("/identity", headers=self.get_basic_auth(username, password))

    def get_basic_auth(self, username, password):
        return {
            'Authorization': 'Basic ' + base64.b64encode(username + ":" + password)
        }


@pytest.fixture
def auth(client):
    return AuthActions(client)


class TaskManager(object):
    def __init__(self, client, auth):
        self._auth = auth
        self._client = client

    def add_task(self, username, password, task):
        task = json.dumps(task)

        headers = self._auth.get_basic_auth(username, password)
        headers["Content-Type"] = "application/json"

        return self._client.post("/tasks", data=task, headers=headers)

    def delete_task(self, username, password, task_idx):
        headers = self._auth.get_basic_auth(username, password)
        return self._client.delete("/tasks/" + str(task_idx), headers=headers)

    def update_task(self, username, password, task, task_idx):
        task = json.dumps(task)

        headers = self._auth.get_basic_auth(username, password)
        headers["Content-Type"] = "application/json"

        return self._client.put("/tasks/" + str(task_idx), data=task, headers=headers)


@pytest.fixture
def task_manager(client, auth):
    return TaskManager(client, auth)
