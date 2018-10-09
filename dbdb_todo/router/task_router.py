from flask import request


class TaskRouter(object):
    @staticmethod
    def router(task_ctrl, app, auth):
        @app.route("/tasks/<int:index>", methods=["PUT"])
        @auth.login_required
        def get_user_taks(index):
            return task_ctrl.update_task(request, index)

        @app.route("/tasks", methods=["POST"])
        @auth.login_required
        def add_user_tasks():
            return task_ctrl.add_task(request)

        @app.route("/tasks/<int:index>", methods=["DELETE"])
        @auth.login_required
        def delete_user_taks(index):
            return task_ctrl.delete_task(request, index)

        return app
