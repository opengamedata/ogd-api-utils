# import libraries
from flask import Flask
from flask_restful import Resource, Api, reqparse
# import locals
from utils.APIResult import APIResult, RESTType, ResultStatus

class HelloAPI:
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(HelloAPI.Hello, '/hello')
        api.add_resource(HelloAPI.ParamHello, '/p_hello/<name>')

    class Hello(Resource):
        def get(self):
            ret_val = APIResult(
                req_type = RESTType.GET,
                val      = None,
                msg      = "Hello! You GETted successfully!",
                status   = ResultStatus.SUCCESS)
            return ret_val.ToDict()

        def post(self):
            ret_val = APIResult(
                req_type = RESTType.POST,
                val      = None,
                msg      = "Hello! You POSTed successfully!",
                status   = ResultStatus.SUCCESS)
            return ret_val.ToDict()

        def put(self):
            ret_val = APIResult(
                req_type = RESTType.PUT,
                val      = None,
                msg      = "Hello! You PUTted successfully!",
                status   = ResultStatus.SUCCESS)
            return ret_val.ToDict()

    class ParamHello(Resource):
        def get(self, name):
            ret_val = APIResult(
                req_type = RESTType.GET,
                val      = None,
                msg      = f"Hello {name}! You GETted successfully!",
                status   = ResultStatus.SUCCESS)
            return ret_val.ToDict()

        def post(self, name):
            ret_val = APIResult(
                req_type = RESTType.POST,
                val      = None,
                msg      = f"Hello {name}! You POSTed successfully!",
                status   = ResultStatus.SUCCESS)
            return ret_val.ToDict()

        def put(self, name):
            ret_val = APIResult(
                req_type = RESTType.PUT,
                val      = None,
                msg      = f"Hello {name}! You PUTted successfully!",
                status   = ResultStatus.SUCCESS)
            return ret_val.ToDict()
