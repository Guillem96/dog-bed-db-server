from flask import request, Response


class UserRouter(object):
    @staticmethod
    def router(user_ctrl, app, auth):
        @auth.get_password
        def get_pw(username):
            return user_ctrl.get_password(username)

        @app.route("/sign-up", methods=["POST"])
        def sign_up():
            return user_ctrl.store(request)

        @app.route("/login", methods=["POST"])
        @auth.login_required
        def login():
            return Response(status=200)

        @app.route("/identity", methods=["GET"])
        @auth.login_required
        def get_user_info():
            return user_ctrl.get(request)

        return app
