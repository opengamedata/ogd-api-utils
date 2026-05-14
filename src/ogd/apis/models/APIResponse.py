"""
APIResponse

Contains class for representing a response from an OGD API,
as well as utility enums used by the APIResponse class.
"""

# import standard libraries
import json
import logging
from typing import Any, Dict, Optional

# import 3rd-party libraries
import requests
from flask import Response

# import OGD libraries
from ogd.common.utils.typing import Map
from ogd.common.utils.Logger import Logger

# Import local files
from ogd.apis.models.enums.RESTType import RESTType
from ogd.apis.models.enums.ResponseStatus import ResponseStatus

class APIResponse:
    def __init__(self, req_type:Optional[RESTType | str], val:Optional[Map], msg:str, status:ResponseStatus):
        self._type   : Optional[RESTType]
        self._val    : Optional[Map]

        if isinstance(req_type, RESTType):
            self._type = req_type
        elif isinstance(req_type, str):
            self._type = RESTType[req_type]
        else:
            self._type = None
        if isinstance(val, dict) or val is None:
            self._val = val
        else:
            try:
                self._val = json.loads(str(val))
            except json.decoder.JSONDecodeError as err:
                abbreviated_val = f"{str(val)[:20]}..." if len(str(val)) > 20 else str(val)
                _msg = f"API response 'value' field contained value '{abbreviated_val}' with invalid type {type(val)}, which could not be converted to a dictionary. Attempting to do so resulted in error:\n{err}\nThe value field will be left blank."
                Logger.Log(_msg, logging.ERROR)
                self._val = None
        self._msg    : str                = msg
        self._status : ResponseStatus     = status

    def __str__(self):
        return f"{str(self.Type)} request: {self.Status}\n{self.Message}\nValues: {self.Value}"

    @staticmethod
    def Default(req_type:RESTType):
        return APIResponse(
            req_type=req_type,
            val=None,
            msg="",
            status=ResponseStatus.NONE
        )

    @staticmethod
    def FromResponse(result:requests.Response) -> "APIResponse":
        ret_val : APIResponse

        try:
            raw = result.json()
            ret_val = APIResponse(req_type=raw.get("type"), val=raw.get("val"), msg=raw.get("msg"), status=ResponseStatus(result.status_code))
        except requests.exceptions.JSONDecodeError:
            ret_val = APIResponse(req_type=None, val=None, msg=result.text, status=ResponseStatus(result.status_code))

        return ret_val
    
    @staticmethod
    def FromDict(all_elements:Dict[str, Any], status:Optional[ResponseStatus]=None) -> Optional["APIResponse"]:
        ret_val : Optional["APIResponse"] = None

        _type_raw   = all_elements.get("type", "NOT FOUND")
        _val_raw    = all_elements.get("val")
        _msg        = all_elements.get("msg", "NOT FOUND")
        _status_raw = all_elements.get("status")
        try:
            _type   = RESTType[str(_type_raw).upper()] if _type_raw else None
            _val    = _val_raw if isinstance(_val_raw, dict) else json.loads(str(_val_raw)) if _val_raw is not None else None
            _status = ResponseStatus[str(_status_raw).upper()] if _status_raw else (status or ResponseStatus.NONE)
        except KeyError:
            pass
        else:
            ret_val = APIResponse(req_type=_type, val=_val, msg=_msg, status=_status)
        return ret_val

    @property
    def Type(self) -> Optional[RESTType]:
        """Property for the type of REST request

        :return: A RESTType representing the type of REST request
        :rtype: _type_
        """
        return self._type

    @property
    def Value(self) -> Optional[Map]:
        """Property for the value of the request result.

        :return: Some value, of any type, returned from the request.
        :rtype: Any
        """
        return self._val
    @Value.setter
    def Value(self, new_val:Optional[Map]):
        self._val = new_val


    @property
    def Message(self) -> str:
        """Property for the message associated with a request result.

        :return: A string message giving details on the result of the request.
        :rtype: str
        """
        return self._msg
    @Message.setter
    def Message(self, new_msg:str):
        self._msg = new_msg

    @property
    def Status(self) -> ResponseStatus:
        """Property for the status of the request.

        :return: A ResponseStatus indicating whether request is/was successful, incomplete, failed, etc.
        :rtype: ResponseStatus
        """
        return self._status
    @property
    def OK(self) -> bool:
        return self.Status in ResponseStatus.SuccessStatuses()

    @property
    def AsDict(self):
        return {
            "type"   : str(self._type),
            "val"    : self._val,
            "msg"    : self._msg,
        }

    @property
    def AsJSON(self):
        return json.dumps(self.AsDict)

    @property
    def AsFlaskResponse(self) -> Response:
        return Response(response=self.AsJSON, status=self.Status.value, mimetype='application/json')

    def RequestErrored(self, msg:str, status:Optional[ResponseStatus]=None):
        self._status = status if status is not None and status in ResponseStatus.ClientErrors() else ResponseStatus.BAD_REQUEST
        self.Message = f"ERROR: {msg}"

    def ServerErrored(self, msg:str, status:Optional[ResponseStatus]=None):
        self._status = status if status is not None and status in ResponseStatus.ServerErrors() else ResponseStatus.INTERNAL_ERR
        self.Message = f"SERVER ERROR: {msg}"

    def RequestSucceeded(self, msg:str, val:Optional[Map]):
        self._status = ResponseStatus.OK
        self.Message = f"SUCCESS: {msg}"
        self.Value   = val
