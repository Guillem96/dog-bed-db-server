from flask import Flask, request, Response
import dbdb
import json

from controller.user_controller import UserController

app = Flask(__name__)
db = dbdb.connect("database.db")
user_ctrl = UserController(db)

@app.route("/login", methods=["POST"])
def login():
	return user_ctrl.login(request)
	
@app.route("/sign-up", methods=["POST"])
def sign_up():
	return user_ctrl.store(request)

if __name__ == "__main__":
	app.run()
