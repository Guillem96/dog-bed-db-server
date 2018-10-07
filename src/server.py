from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth

import dbdb
import json

from controller.user_controller import UserController
from controller.task_contrller import TaskController

app = Flask(__name__)
auth = HTTPBasicAuth()

db = dbdb.connect("database.db")
user_ctrl = UserController(db)
task_ctrl = TaskController(db, user_ctrl)

@auth.get_password
def get_pw(username):
    return user_ctrl.get_password(username)

@app.route("/login", methods=["POST"])
def login():
	return user_ctrl.login(request)
	
@app.route("/sign-up", methods=["POST"])
def sign_up():
	return user_ctrl.store(request)

@app.route("/<username>", methods=["GET"])
def get_user_info(username):
	return user_ctrl.get(username)

@app.route("/<username>/tasks", methods=["GET"])
@auth.login_required
def get_user_taks(username):
	return user_ctrl.get_tasks(username)

@app.route("/<username>/tasks", methods=["POST"])
@auth.login_required
def add_user_taks(username):
	return task_ctrl.store(request, username)

if __name__ == "__main__":
	app.run()
