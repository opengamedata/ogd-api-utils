# import libraries
import json
import logging
import requests
import unittest
from unittest import TestCase
# import 3rd-party libraries
from flask import Flask
# import ogd-core libraries.
from ogd.apis.models.APIRequest import APIRequest
from ogd.apis.models.APIResponse import APIResponse
from ogd.common.configs.TestConfig import TestConfig
from ogd.common.utils.Logger import Logger
# import locals
from ogd.apis.configs.ServerConfig import ServerConfig
from ogd.apis.HelloAPI import HelloAPI
from tests.config.t_config import settings

class RemoteCase(TestCase):
    DEFAULT_ADDRESS = "127.0.0.1:5000"

    @classmethod
    def setUpClass(cls) -> None:
        testing_config = TestConfig.FromDict(name="HelloAPITestConfig", unparsed_elements=settings)
        cls.base_url = testing_config.NonStandardElements.get("REMOTE_ADDRESS", RemoteCase.DEFAULT_ADDRESS)

        _level = logging.DEBUG if testing_config.Verbose else logging.INFO
        Logger.InitializeLogger(level=_level, use_logfile=False)

    # @unittest.skip("Not yet set up to test Version remotely.")
    def test_get(self):
        _url = f"{self.base_url}/version"
        try:
            result : APIResponse = APIRequest(url=_url, request_type="GET", params={}).Execute(logger=Logger.std_logger)
        except Exception as err: # pylint: disable=broad-exception-caught
            self.fail(str(err))
        else:
            self.assertIsNotNone(result, f"No response from {_url}")
            self.assertTrue(result.OK, f"Bad status from {_url}")
            self.assertEqual(str(result.Type), "GET", f"Bad type from {_url}")
            self.assertEqual(result.Value, {"version": "0.0.0-Testing"}, f"Bad val from {_url}")
            self.assertEqual(result.Message, "Successfully retrieved API version.", f"Bad msg from {_url}")
