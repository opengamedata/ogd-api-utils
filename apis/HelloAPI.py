# Global imports
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse

class HelloAPI:
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(HelloAPI.Hello, '/hello')
        api.add_resource(HelloAPI.ParamHello, '/p_hello/<name>')

    class Hello(Resource):
        def get(self):
            ret_val = {
                "message":"Hello! You GETted successfully!"
            }
            return ret_val

        def post(self):
            ret_val = {
                "message":"Hello! You POSTed successfully!"
            }
            return ret_val

        def put(self):
            ret_val = {
                "message":"Hello! You PUTted successfully!"
            }
            return ret_val

    class ParamHello(Resource):
        def get(self, name):
            ret_val = {
                "message":f"Hello {name}! You GETted successfully!"
            }
            return ret_val

        def post(self, name):
            ret_val = {
                "message":f"Hello {name}! You POSTed successfully!"
            }
            return ret_val

        def put(self, name):
            ret_val = {
                "message":f"Hello {name}! You PUTted successfully!"
            }
            return ret_val
