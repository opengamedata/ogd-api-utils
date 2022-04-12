from enum import IntEnum
from typing import Any

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
            return "INVALID"

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
            return "INVALID"

class APIResult:
    def __init__(self, req_type:RESTType, val:Any, msg:str, status:ResultStatus):
        self._type   : RESTType     = req_type
        self._val    : Any          = val
        self._msg    : str          = msg
        self._status : ResultStatus = status

    @staticmethod
    def Default(req_type:RESTType):
        return APIResult(
            req_type=req_type,
            val=None,
            msg="",
            status=ResultStatus.NONE
        )

    def RequestErrored(self, msg:str):
        self._status = ResultStatus.ERR_REQ
        self._msg = msg

    def ServerErrored(self, msg:str):
        self._status = ResultStatus.ERR_SRV
        self._msg = msg

    def RequestSucceeded(self, msg:str, val:Any):
        self._status = ResultStatus.SUCCESS
        self._msg = msg
        self._val = val

    def ToDict(self):
        return {
            "type"   : str(self._type),
            "val"    : self._val,
            "msg"    : self._msg,
            "status" : str(self._status)
        }

    def Type(self):
        return self._type

    def Value(self):
        return self._val

    def Message(self):
        return self._msg

    def Status(self):
        return self._status

    def SetType(self, new_type:RESTType):
        self._type = new_type

    def SetValue(self, new_val:Any):
        self._val = new_val

    def SetMessage(self, new_msg:str):
        self._msg = new_msg

    def SetStatus(self, new_status:ResultStatus):
        self._status = new_status