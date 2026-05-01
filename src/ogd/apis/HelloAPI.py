"""
HelloAPI

Contains the HelloAPI class, which we register to all API apps as a way to test that the app is active.
"""

# import libraries

# import 3rd-party libraries
from flask import Flask
from flask_restful import Resource, Api

# import OGD libraries

# import locals
from ogd.apis.resources.Hello import Hello
from ogd.apis.resources.ParamHello import ParamHello
from ogd.apis.configs.ServerConfig import ServerConfig
from ogd.apis.models.enums.ResponseStatus import ResponseStatus
from ogd.apis.models.enums.RESTType import RESTType
from ogd.apis.models.APIResponse import APIResponse

class HelloAPI:
    @staticmethod
    def register(app:Flask, server_config:ServerConfig):
        api = Api(app)
        api.add_resource(Hello, '/hello')
        api.add_resource(ParamHello, '/p_hello/<name>')
        api.add_resource(HelloAPI.Version, '/version')

        HelloAPI.server_config = server_config

    class Version(Resource):
        def get(self):
            ret_val = APIResponse(
                req_type = RESTType.GET,
                val      = { "version" : str(HelloAPI.server_config.Version) },
                msg      = f"Successfully retrieved API version.",
                status   = ResponseStatus.OK)
            return ret_val.AsDict
