from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth

import dbdb
import json
import os

from controller.user_controller import UserController


def init_db(app):
	db = dbdb.connect(app.config["DATABASE"])
	return db

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)
	auth = HTTPBasicAuth()
	app.config.from_mapping(DATABASE='database.db')
	
	if test_config:
		app.config.from_mapping(test_config)
	
	db = init_db(app)
	user_ctrl = UserController(db)

	@auth.get_password
	def get_pw(username):
		return user_ctrl.get_password(username)


	@app.route('/')
	def home():
		return "<h1>Hello world!</h1>"

	@app.route("/login", methods=["POST"])
	def login():
		return user_ctrl.login(request)
		
	@app.route("/sign-up", methods=["POST"])
	def sign_up():
		return user_ctrl.store(request)

	@app.route("/identity", methods=["GET"])
	def get_user_info():
		return user_ctrl.get(auth.username())

	@app.route("/tasks", methods=["GET"])
	@auth.login_required
	def get_user_taks():
		return user_ctrl.get_tasks(auth.username())

	@app.route("/tasks", methods=["POST"])
	@auth.login_required
	def add_user_taks():
		return user_ctrl.add_task(request)

	@app.route("/tasks/<int:index>", methods=["DELETE"])
	@auth.login_required
	def delete_user_taks(index):
		return user_ctrl.delete_task(request, index)

	return app

app = create_app()