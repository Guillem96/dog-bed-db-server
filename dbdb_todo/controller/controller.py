import json
from flask import Response


class Controller(object):
    def process_request(self, request, process, index=-1):
        username = None
        if request.authorization:
            username = request.authorization.get("username")

        if request.method in {'POST', 'PUT'} and not request.data:
            return Response('{ "msg": "Json body is required" }', status=400)

        try:
            data = request.data and json.loads(request.data)
            return process(data, username=username, index=index)
        except KeyError:
            return Response('{ "msg": "Properties missing" }', status=400)
        except (UnicodeDecodeError, ValueError):
            return Response('{ "msg": "Json body is required" }', status=400)
