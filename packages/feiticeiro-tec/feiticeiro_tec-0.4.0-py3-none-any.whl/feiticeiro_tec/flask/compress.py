
from flask import Flask, request
import gzip
from functools import wraps


class Compress:
    def __init__(self, app: Flask):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app.after_request(self.after_request)

    @classmethod
    def after_request(cls, response):
        if request.headers.get("Accept-Encoding", "") != "gzip":
            return response
        if (
            response.status_code < 200
            or response.status_code >= 300
            or "Content-Encoding" in response.headers
        ):
            return response
        response.data = gzip.compress(response.data)
        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = len(response.data)
        return response

    def compress_decorator(self, function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            response = function(*args, **kwargs)
            return self.after_request(response)

        return decorated_function
