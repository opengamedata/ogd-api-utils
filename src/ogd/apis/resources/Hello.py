# import 3rd-party libraries
from flask_restful import Resource

from ogd.apis.models.APIResponse import APIResponse, RESTType, ResponseStatus

class Hello(Resource):
    def get(self):
        ret_val = APIResponse(
            req_type = RESTType.GET,
            val      = None,
            msg      = "Hello! You GETted successfully!",
            status   = ResponseStatus.OK)
        return ret_val.AsDict

    def post(self):
        ret_val = APIResponse(
            req_type = RESTType.POST,
            val      = None,
            msg      = "Hello! You POSTed successfully!",
            status   = ResponseStatus.OK)
        return ret_val.AsDict

    def put(self):
        ret_val = APIResponse(
            req_type = RESTType.PUT,
            val      = None,
            msg      = "Hello! You PUTted successfully!",
            status   = ResponseStatus.OK)
        return ret_val.AsDict
