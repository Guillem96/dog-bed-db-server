import pytest
import json

def test_add_task(auth, task_manager):
	res = auth.sign_up("guillem", "pw", "guillem@email.com")
	assert res.status_code == 201

	new_task = dict(
		name="Flask server",
		description="End up with flask backend using dbdb",
		date_limit="15/10/2018"
	)
	res = task_manager.add_task("guillem", "pw", new_task)
	assert res.status_code == 201

	res_data = json.loads(res.data)
	assert len(res_data["tasks"]) == 1
	assert res_data["tasks"][0]["name"] == "Flask server"

def test_add_task_wo_auth(auth, task_manager):
	res = auth.sign_up("guillem", "pw", "guillem@email.com")
	assert res.status_code == 201
	
	new_task = dict(
		name="Flask server",
		description="End up with flask backend using dbdb",
		date_limit="15/10/2018"
	)
	res = task_manager.add_task("guillem", "bad_pass", new_task)
	assert res.status_code == 401

	res = auth.identity("guillem", "pw")
	res_data = json.loads(res.data)
	assert len(res_data["tasks"]) == 0

def test_add_2_or_mre_task(auth, task_manager):
	res = auth.sign_up("guillem", "pw", "guillem@email.com")
	assert res.status_code == 201
	
	new_task = dict(
		name="Flask server",
		description="End up with flask backend using dbdb",
		date_limit="15/10/2018"
	)
		
	another_task = dict(
		name="Flask client",
		description="End up with flask backend using dbdb",
		date_limit="15/10/2018"
	)
	
	res = task_manager.add_task("guillem", "pw", new_task)
	assert res.status_code == 201
	
	res = task_manager.add_task("guillem", "pw", another_task)
	assert res.status_code == 201
	
	res_data = json.loads(res.data)
	assert len(res_data["tasks"]) == 2

def test_delete_task(auth, task_manager):
	res = auth.sign_up("guillem", "pw", "guillem@email.com")
	assert res.status_code == 201
	
	new_task = dict(
		name="Flask server",
		description="End up with flask backend using dbdb",
		date_limit="15/10/2018"
	)
		
	another_task = dict(
		name="Flask client",
		description="End up with flask backend using dbdb",
		date_limit="15/10/2018"
	)
	
	res = task_manager.add_task("guillem", "pw", new_task)
	assert res.status_code == 201
	
	res = task_manager.add_task("guillem", "pw", another_task)
	assert res.status_code == 201

	res = task_manager.delete_task("guillem", "pw", 0)
	res_data = json.loads(res.data)

	assert len(res_data["tasks"]) == 1
	assert res_data["tasks"][0]["name"] == "Flask client"

