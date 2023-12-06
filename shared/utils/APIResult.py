import json
from enum import IntEnum
from typing import Any
from grpc import Status
# Import local files
import ogd.core.requests.RequestResult as RequestResult

class RESTType(IntEnum):
    """Simple enumerated type to track type of a REST request.
    """
    GET = 1
    POST = 2
    PUT = 3

    def __str__(self):
        """Stringify function for RESTTypes.

        :return: Simple string version of the name of a RESTType
        :rtype: _type_
        """
        if self.value == RESTType.GET:
            return "GET"
        elif self.value == RESTType.POST:
            return "POST"
        elif self.value == RESTType.PUT:
            return "PUT"
        else:
            return "INVALID REST TYPE"

class ResultStatus(IntEnum):
    """Simple enumerated type to track the status of an API request result.
    """
    NONE = 1
    SUCCESS = 2
    ERR_SRV = 3
    ERR_REQ = 4

    def __str__(self):
        """Stringify function for ResultStatus objects.

        :return: Simple string version of the name of a ResultStatus
        :rtype: _type_
        """
        if self.value == ResultStatus.NONE:
            return "NONE"
        elif self.value == ResultStatus.SUCCESS:
            return "SUCCESS"
        elif self.value == ResultStatus.ERR_SRV:
            return "SERVER ERROR"
        elif self.value == ResultStatus.ERR_REQ:
            return "REQUEST ERROR"
        else:
            return "INVALID STATUS TYPE"

class APIResult:
    def __init__(self, req_type:RESTType, val:Any, msg:str, status:ResultStatus):
        self._type   : RESTType     = req_type
        self._val    : Any          = val
        self._msg    : str          = msg
        self._status : ResultStatus = status

    def __str__(self):
        return f"{self.Type.name} request: {self.Status}\n{self.Message}\nValues: {self.Value}"

    @staticmethod
    def Default(req_type:RESTType):
        return APIResult(
            req_type=req_type,
            val=None,
            msg="",
            status=ResultStatus.NONE
        )

    @staticmethod
    def FromRequestResult(result:RequestResult.RequestResult, req_type:RESTType):
        _status : ResultStatus
        if result.Status == RequestResult.ResultStatus.SUCCESS:
            _status = ResultStatus.SUCCESS 
        elif result.Status == RequestResult.ResultStatus.FAILURE:
            _status = ResultStatus.ERR_REQ
        else:
            _status = ResultStatus.ERR_SRV
        ret_val = APIResult(req_type=req_type, val=None, msg=result.Message, status=_status)
        return ret_val

    @property
    def Type(self) -> RESTType:
        """Property for the type of REST request

        :return: A RESTType representing the type of REST request
        :rtype: _type_
        """
        return self._type

    @property
    def Value(self) -> Any:
        """Property for the value of the request result.

        :return: Some value, of any type, returned from the request.
        :rtype: Any
        """
        return self._val
    @Value.setter
    def Value(self, new_val:Any):
        self._val = new_val


    @property
    def Message(self) -> str:
        """Property for the message associated with a request result.

        :return: A string message giving details on the result of the request.
        :rtype: str
        """
        return self._msg

    @property
    def Status(self) -> ResultStatus:
        """Property for the status of the request.

        :return: A ResultStatus indicating whether request is/was successful, incomplete, failed, etc.
        :rtype: ResultStatus
        """
        return self._status

    def RequestErrored(self, msg:str):
        self._status = ResultStatus.ERR_REQ
        self._msg = f"ERROR: {msg}"

    def ServerErrored(self, msg:str):
        self._status = ResultStatus.ERR_SRV
        self._msg = f"SERVER ERROR: {msg}"

    def RequestSucceeded(self, msg:str, val:Any):
        self._status = ResultStatus.SUCCESS
        self._msg = f"SUCCESS: {msg}"
        self._val = val

    def ToDict(self):
        return {
            "type"   : str(self._type),
            "val"    : self._val,
            "msg"    : self._msg,
            "status" : str(self._status)
        }
