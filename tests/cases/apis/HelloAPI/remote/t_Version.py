# import libraries
import json
import logging
import requests
import unittest
from unittest import TestCase
# import 3rd-party libraries
from flask import Flask
# import ogd-core libraries.
from ogd.common.configs.TestConfig import TestConfig
from ogd.common.utils.Logger import Logger
# Logger.InitializeLogger(level=logging.INFO, use_logfile=False)
# import locals
from ogd.apis.configs.ServerConfig import ServerConfig
from ogd.apis.HelloAPI import HelloAPI
from tests.config.t_config import settings

class t_Version_remote(TestCase):
    DEFAULT_ADDRESS = "127.0.0.1:5000"

    @classmethod
    def setUpClass(cls) -> None:
        testing_config = TestConfig.FromDict(name="HelloAPITestConfig", unparsed_elements=settings)
        cls.base_url = testing_config.NonStandardElements.get("REMOTE_ADDRESS", t_Version_remote.DEFAULT_ADDRESS)

        _level = logging.DEBUG if testing_config.Verbose else logging.INFO
        Logger.std_logger.setLevel(_level)

    @unittest.skip("Not yet set up to test Version remotely.")
    def test_get(self):
        _url = f"{self.base_url}/version"
        Logger.Log(f"GET test at {_url}", logging.DEBUG)
        try:
            result = requests.get(url=_url)
        except Exception as err:
            self.fail(str(err))
        else:
            Logger.Log(f"Result: status '{result.status_code}', and data <{result.json()}>", logging.DEBUG)
            self.assertNotEqual(result, None)
