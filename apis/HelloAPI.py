# Global imports
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse
# Local imports
from config.config import settings

class HelloAPI:
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(HelloAPI.Hello, '/hello')
        api.add_resource(HelloAPI.ParamHello, '/p_hello/<name>')

    class Hello(Resource):
        def get(self):
            ret_val = {
                "type":"GET",
                "val":None,
                "msg":"Hello! You GETted successfully!",
                "status":"SUCCESS",
                "version":settings['VER']
            }
            return ret_val

        def post(self):
            ret_val = {
                "type":"POST",
                "val":None,
                "msg":"Hello! You POSTed successfully!",
                "status":"SUCCESS",
                "version":settings['VER']
            }
            return ret_val

        def put(self):
            ret_val = {
                "type":"PUT",
                "val":None,
                "msg":"Hello! You PUTted successfully!",
                "status":"SUCCESS",
                "version":settings['VER']
            }
            return ret_val

    class ParamHello(Resource):
        def get(self, name):
            ret_val = {
                "type":"GET",
                "val":None,
                "msg":f"Hello {name}! You GETted successfully!",
                "status":"SUCCESS",
                "version":settings['VER']
            }
            return ret_val

        def post(self, name):
            ret_val = {
                "type":"POST",
                "val":None,
                "msg":f"Hello {name}! You POSTed successfully!",
                "status":"SUCCESS",
                "version":settings['VER']
            }
            return ret_val

        def put(self, name):
            ret_val = {
                "type":"PUT",
                "val":None,
                "msg":f"Hello {name}! You PUTted successfully!",
                "status":"SUCCESS",
                "version":settings['VER']
            }
            return ret_val
