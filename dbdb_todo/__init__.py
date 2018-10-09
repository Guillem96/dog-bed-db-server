from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

import dbdb
import json
import os

from router.task_router import TaskRouter
from router.user_router import UserRouter

from controller.user_controller import UserController
from controller.task_controller import TaskController


def init_db(app):
    db = dbdb.connect(app.config["DATABASE"])
    return db


def create_app(test_config=None):
    app = Flask(__name__)
    auth = HTTPBasicAuth()
    app.config.from_mapping(DATABASE='database.db')

    if test_config:
        app.config.from_mapping(test_config)

    db = init_db(app)
    user_ctrl = UserController(db)
    task_ctrl = TaskController(db, user_ctrl)

    app = UserRouter.router(user_ctrl, app, auth)
    app = TaskRouter.router(task_ctrl, app, auth)

    return app


app = create_app()
CORS(app)
