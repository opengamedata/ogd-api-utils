# import 3rd-party libraries
from flask_restful import Resource

from ogd.apis.models.APIResponse import APIResponse, RESTType, ResponseStatus

class ParamHello(Resource):
    def get(self, name):
        ret_val = APIResponse(
            req_type = RESTType.GET,
            val      = None,
            msg      = f"Hello {name}! You GETted successfully!",
            status   = ResponseStatus.OK)
        return ret_val.AsDict

    def post(self, name):
        ret_val = APIResponse(
            req_type = RESTType.POST,
            val      = None,
            msg      = f"Hello {name}! You POSTed successfully!",
            status   = ResponseStatus.OK)
        return ret_val.AsDict

    def put(self, name):
        ret_val = APIResponse(
            req_type = RESTType.PUT,
            val      = None,
            msg      = f"Hello {name}! You PUTted successfully!",
            status   = ResponseStatus.OK)
        return ret_val.AsDict
