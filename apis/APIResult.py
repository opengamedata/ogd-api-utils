from enum import Enum
from typing import Any, Union

class RESTType(Enum):
    GET = 1
    POST = 2
    PUT = 3

class ResultStatus(Enum):
    NONE = 1
    SUCCESS = 2
    ERR_SRV = 3
    ERR_REQ = 4

class APIResult:
    RESTtoString = {1:"GET", 2:"POST", 3:"PUT"}
    StatusString = {1:"DID_NOTHING", 2:"SUCCESS", 3:"ERR_SRV", 4:"ERR_REQ"}

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
            "type"   : APIResult.RESTtoString[self._type.value],
            "val"    : self._val,
            "msg"    : self._msg,
            "status" : APIResult.StatusString[self._status.value]
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