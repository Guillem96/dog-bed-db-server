import pytest
import json

new_task = dict(
    name="Flask server",
    description="End up with flask backend using dbdb",
    date_limit="15/10/2018",
    tags=["University"]
)

another_task = dict(
    name="Flask client",
    description="End up with flask backend using dbdb",
    date_limit="15/10/2018",
    tags=["University"]
)


def test_add_task(auth, task_manager):
    res = auth.sign_up("Guillem", "Orellana", "guillem",
                       "pw", "guillem@email.com")
    assert res.status_code == 201

    res = task_manager.add_task("guillem", "pw", new_task)
    assert res.status_code == 201

    res_data = json.loads(res.data)
    assert len(res_data["tasks"]) == 1
    assert len(res_data["tasks"][0]["tags"]) == 1
    assert res_data["tasks"][0]["tags"][0] == "University"
    assert res_data["tasks"][0]["name"] == "Flask server"


def test_add_task_wo_auth(auth, task_manager):
    res = auth.sign_up("Guillem", "Orellana", "guillem",
                       "pw", "guillem@email.com")
    assert res.status_code == 201

    res = task_manager.add_task("guillem", "bad_pass", new_task)
    assert res.status_code == 401

    res = auth.identity("guillem", "pw")
    res_data = json.loads(res.data)
    assert len(res_data["tasks"]) == 0


def test_add_2_or_mre_task(auth, task_manager):
    res = auth.sign_up("Guillem", "Orellana", "guillem",
                       "pw", "guillem@email.com")
    assert res.status_code == 201

    res = task_manager.add_task("guillem", "pw", new_task)
    assert res.status_code == 201

    res = task_manager.add_task("guillem", "pw", another_task)
    assert res.status_code == 201

    res_data = json.loads(res.data)
    assert len(res_data["tasks"]) == 2


def test_delete_task(auth, task_manager):
    res = auth.sign_up("Guillem", "Orellana", "guillem",
                       "pw", "guillem@email.com")
    assert res.status_code == 201

    res = task_manager.add_task("guillem", "pw", new_task)
    assert res.status_code == 201

    res = task_manager.add_task("guillem", "pw", another_task)
    assert res.status_code == 201

    res = task_manager.delete_task("guillem", "pw", 0)
    res_data = json.loads(res.data)

    assert len(res_data["tasks"]) == 1
    assert res_data["tasks"][0]["name"] == "Flask client"


def test_concurrent_users(auth, task_manager):
    res = auth.sign_up("Guillem", "Orellana", "guillem",
                       "pw", "guillem@email.com")
    assert res.status_code == 201

    res = auth.sign_up("Another", "one", "another",
                       "pw", "another@email.com")
    assert res.status_code == 201

    # Guilem adds a task
    res = task_manager.add_task("guillem", "pw", new_task)
    res_data = json.loads(res.data)
    assert len(res_data["tasks"]) == 1

    # Another adds 2 tasks
    res = task_manager.add_task("another", "pw", another_task)
    assert res.status_code == 201
    res = task_manager.add_task("another", "pw", new_task)
    assert res.status_code == 201
    res_data = json.loads(res.data)
    assert len(res_data["tasks"]) == 2

    # Then guillem check its tasks
    res = auth.identity("guillem", "pw")
    res_data = json.loads(res.data)
    assert len(res_data["tasks"]) == 1
    assert res_data["tasks"][0]["name"] == new_task["name"]

    # Then another check its tasks
    res = auth.identity("another", "pw")
    res_data = json.loads(res.data)
    assert len(res_data["tasks"]) == 2
    assert res_data["tasks"][0]["name"] == another_task["name"]


def test_update_task(auth, task_manager):
    res = auth.sign_up("Guillem", "Orellana", "guillem",
                       "pw", "guillem@email.com")
    assert res.status_code == 201

    res = task_manager.add_task("guillem", "pw", new_task)
    assert res.status_code == 201

    res = task_manager.add_task("guillem", "pw", another_task)
    assert res.status_code == 201

    res_data = json.loads(res.data)
    task = res_data["tasks"][0]
    task["done"] = True

    res = task_manager.update_task("guillem", "pw", task, 0)
    assert res.status_code == 200

    res_data = json.loads(res.data)
    assert res_data["tasks"][0]["done"] == True
