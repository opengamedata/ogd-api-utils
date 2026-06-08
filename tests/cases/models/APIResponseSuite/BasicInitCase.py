# import libraries
import json
import logging
import unittest
from pathlib import Path
from unittest import TestCase
# import ogd libraries
from ogd.common.configs.TestConfig import TestConfig
from ogd.common.utils.Logger import Logger
# import locals
from ogd.apis.models.enums.ResponseStatus import ResponseStatus
from ogd.apis.models.enums.RESTType import RESTType
from ogd.apis.models.APIResponse import APIResponse
from tests.config.t_config import settings


class t_APIResponse(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _config = TestConfig.FromDict(name="APIResponseTestConfig", unparsed_elements=settings)
        _level = logging.DEBUG if _config.Verbose else logging.INFO
        Logger.InitializeLogger(level=_level, use_logfile=False)
        
    def setUp(self):
        self.response : APIResponse = APIResponse(req_type=RESTType.GET, val={"foo":"bar"}, msg="Complete", status=ResponseStatus.OK)

    @unittest.skip("Not yet implemented")
    def test_FromRequestResult(self):
        pass

    # TODO : we could just do a different setUp(...) function in a sub-class of t_APIResponse, I think, instead of repeating every line of every property test.
    def test_FromFromDict_recall(self):
        _response = APIResponse.FromDict(self.response.AsDict, status=ResponseStatus.OK)
        if _response:
            self.assertEqual(_response.Type, RESTType.GET)
            self.assertEqual(_response.Value, {"foo":"bar"})
            self.assertEqual(_response.Message, "Complete")
            self.assertEqual(_response.Status, ResponseStatus.OK)
        else:
            self.fail("_response was None, failure in parsing FromDict!")

    def test_FromFromDict_recall_nostatus(self):
        _response = APIResponse.FromDict(self.response.AsDict)
        if _response:
            self.assertEqual(_response.Type, RESTType.GET)
            self.assertEqual(_response.Value, {"foo":"bar"})
            self.assertEqual(_response.Message, "Complete")
            self.assertEqual(_response.Status, ResponseStatus.NONE)
        else:
            self.fail("_response was None, failure in parsing FromDict!")

    def test_Type(self):
        self.assertEqual(self.response.Type, RESTType.GET)

    def test_Value(self):
        self.assertEqual(self.response.Value, {"foo":"bar"})

    def test_Message(self):
        self.assertEqual(self.response.Message, "Complete")

    def test_Status(self):
        self.assertEqual(self.response.Status, ResponseStatus.OK)

    def test_AsDict(self):
        expected = {
            "type": "GET",
            "val": {"foo":"bar"},
            "msg": "Complete"
        }
        d = self.response.AsDict
        for key in expected.keys():
            self.assertIn(key, d.keys(), f"Response is missing key {key}")
            self.assertEqual(d[key], expected[key])

    def test_AsJSON(self):
        expected = {
            "type": "GET",
            "val": {"foo":"bar"},
            "msg": "Complete"
        }
        self.assertEqual(self.response.AsJSON, json.dumps(expected))

    @unittest.skip("Not yet implemented")
    def test_AsFlaskResponse(self):
        pass

    def test_RequestErrored_default_status(self):
        self.response.RequestErrored("Default request error")
        self.assertEqual(self.response.Message, "ERROR: Default request error")
        self.assertEqual(self.response.Status, ResponseStatus.BAD_REQUEST)

    def test_RequestErrored_general_status(self):
        self.response.RequestErrored("General request error", ResponseStatus.BAD_REQUEST)
        self.assertEqual(self.response.Message, "ERROR: General request error")
        self.assertEqual(self.response.Status, ResponseStatus.BAD_REQUEST)

    def test_RequestErrored_notfound_status(self):
        self.response.RequestErrored("404 request error", ResponseStatus.NOT_FOUND)
        self.assertEqual(self.response.Message, "ERROR: 404 request error")
        self.assertEqual(self.response.Status, ResponseStatus.NOT_FOUND)

    def test_RequestErrored_invalid_status(self):
        self.response.RequestErrored("Invalid choice of code for request error, should give default error code", ResponseStatus.INTERNAL_ERR)
        self.assertEqual(self.response.Message, "ERROR: Invalid choice of code for request error, should give default error code")
        self.assertEqual(self.response.Status, ResponseStatus.BAD_REQUEST)

    def test_ServerErrored_default_status(self):
        self.response.ServerErrored("Default server error")
        self.assertEqual(self.response.Message, "SERVER ERROR: Default server error")
        self.assertEqual(self.response.Status, ResponseStatus.INTERNAL_ERR)

    def test_ServerErrored_general_status(self):
        self.response.ServerErrored("General server error")
        self.assertEqual(self.response.Message, "SERVER ERROR: General server error", ResponseStatus.INTERNAL_ERR)
        self.assertEqual(self.response.Status, ResponseStatus.INTERNAL_ERR)

    def test_ServerErrored_invalid_status(self):
        self.response.ServerErrored("Invalid choice of code for server error, should give default error code", ResponseStatus.BAD_REQUEST)
        self.assertEqual(self.response.Message, "SERVER ERROR: Invalid choice of code for server error, should give default error code")
        self.assertEqual(self.response.Status, ResponseStatus.INTERNAL_ERR)

    def test_RequestSucceeded(self):
        self.response.RequestSucceeded(msg="Default server success", val={"foo":"bar"})
        self.assertEqual(self.response.Message, "SUCCESS: Default server success")
        self.assertEqual(self.response.Status, ResponseStatus.OK)
        self.assertEqual(self.response.Value, {"foo":"bar"})

if __name__ == '__main__':
    unittest.main()
