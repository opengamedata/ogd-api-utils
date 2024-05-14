"""
HelloAPI

Contains the HelloAPI class, which we register to all API apps as a way to test that the app is active.
"""

# import libraries

# import 3rd-party libraries
from flask import Flask
from flask_restful import Resource, Api, reqparse

# import OGD libraries
from ogd.apis.utils.APIResponse import APIResponse, RESTType, ResponseStatus

# import locals

class HelloAPI:
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(HelloAPI.Hello, '/hello')
        api.add_resource(HelloAPI.ParamHello, '/p_hello/<name>')

    class Hello(Resource):
        def get(self):
            ret_val = APIResponse(
                req_type = RESTType.GET,
                val      = None,
                msg      = "Hello! You GETted successfully!",
                status   = ResponseStatus.SUCCESS)
            return ret_val.AsDict

        def post(self):
            ret_val = APIResponse(
                req_type = RESTType.POST,
                val      = None,
                msg      = "Hello! You POSTed successfully!",
                status   = ResponseStatus.SUCCESS)
            return ret_val.AsDict

        def put(self):
            ret_val = APIResponse(
                req_type = RESTType.PUT,
                val      = None,
                msg      = "Hello! You PUTted successfully!",
                status   = ResponseStatus.SUCCESS)
            return ret_val.AsDict

    class ParamHello(Resource):
        def get(self, name):
            ret_val = APIResponse(
                req_type = RESTType.GET,
                val      = None,
                msg      = f"Hello {name}! You GETted successfully!",
                status   = ResponseStatus.SUCCESS)
            return ret_val.AsDict

        def post(self, name):
            ret_val = APIResponse(
                req_type = RESTType.POST,
                val      = None,
                msg      = f"Hello {name}! You POSTed successfully!",
                status   = ResponseStatus.SUCCESS)
            return ret_val.AsDict

        def put(self, name):
            ret_val = APIResponse(
                req_type = RESTType.PUT,
                val      = None,
                msg      = f"Hello {name}! You PUTted successfully!",
                status   = ResponseStatus.SUCCESS)
            return ret_val.AsDict
