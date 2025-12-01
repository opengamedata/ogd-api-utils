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
from src.ogd.apis.utils.APIResponse import APIResponse, RESTType, ResponseStatus
from tests.config.t_config import settings


class t_APIResponse(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _config = TestConfig.FromDict(name="APIResponseTestConfig", unparsed_elements=settings)
        _level = logging.DEBUG if _config.Verbose else logging.INFO
        Logger.InitializeLogger(level=_level, use_logfile=False)
        
    def setUp(self):
        self.response = APIResponse(req_type=RESTType.GET, val={"foo":"bar"}, msg="Complete", status=ResponseStatus.SUCCESS)

    @unittest.skip("Not yet implemented")
    def test_FromRequestResult(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_FromFromDict(self):
        pass

    def test_Type(self):
        self.assertEqual(self.response.Type, RESTType.GET)

    def test_Value(self):
        self.assertEqual(self.response.Value, {"foo":"bar"})

    def test_Message(self):
        self.assertEqual(self.response.Message, "Complete")

    def test_Status(self):
        self.assertEqual(self.response.Status, ResponseStatus.SUCCESS)

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
        self.assertEqual(self.response.Status, ResponseStatus.ERR_REQ)

    def test_RequestErrored_general_status(self):
        self.response.RequestErrored("General request error", ResponseStatus.ERR_REQ)
        self.assertEqual(self.response.Message, "ERROR: General request error")
        self.assertEqual(self.response.Status, ResponseStatus.ERR_REQ)

    def test_RequestErrored_notfound_status(self):
        self.response.RequestErrored("404 request error", ResponseStatus.ERR_NOTFOUND)
        self.assertEqual(self.response.Message, "ERROR: 404 request error")
        self.assertEqual(self.response.Status, ResponseStatus.ERR_NOTFOUND)

    def test_RequestErrored_invalid_status(self):
        self.response.RequestErrored("Invalid choice of code for request error, should give default error code", ResponseStatus.ERR_SRV)
        self.assertEqual(self.response.Message, "ERROR: Invalid choice of code for request error, should give default error code")
        self.assertEqual(self.response.Status, ResponseStatus.ERR_REQ)

    def test_ServerErrored_default_status(self):
        self.response.ServerErrored("Default server error")
        self.assertEqual(self.response.Message, "SERVER ERROR: Default server error")
        self.assertEqual(self.response.Status, ResponseStatus.ERR_SRV)

    def test_ServerErrored_general_status(self):
        self.response.ServerErrored("General server error")
        self.assertEqual(self.response.Message, "SERVER ERROR: General server error", ResponseStatus.ERR_SRV)
        self.assertEqual(self.response.Status, ResponseStatus.ERR_SRV)

    def test_ServerErrored_invalid_status(self):
        self.response.ServerErrored("Invalid choice of code for server error, should give default error code", ResponseStatus.ERR_REQ)
        self.assertEqual(self.response.Message, "SERVER ERROR: Invalid choice of code for server error, should give default error code")
        self.assertEqual(self.response.Status, ResponseStatus.ERR_SRV)

    def test_RequestSucceeded(self):
        self.response.RequestSucceeded(msg="Default server success", val={"foo":"bar"})
        self.assertEqual(self.response.Message, "SUCCESS: Default server success")
        self.assertEqual(self.response.Status, ResponseStatus.SUCCESS)
        self.assertEqual(self.response.Value, {"foo":"bar"})

if __name__ == '__main__':
    unittest.main()
