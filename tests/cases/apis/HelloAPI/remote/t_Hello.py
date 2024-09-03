# import libraries
import json
import logging
import requests
import unittest
from unittest import TestCase
# import 3rd-party libraries
from flask import Flask
# import ogd-core libraries.
from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
from ogd.core.utils.Logger import Logger
# import locals
from src.ogd.apis.schemas.ServerConfigSchema import ServerConfigSchema
from src.ogd.apis.utils.TestRequest import TestRequest
from src.ogd.apis.HelloAPI import HelloAPI
from tests.config.t_config import settings

class t_Hello_remote(TestCase):
    DEFAULT_ADDRESS = "127.0.0.1:5000"

    @classmethod
    def setUpClass(cls) -> None:
        cls.testing_config = TestConfigSchema.FromDict(name="HelloAPITestConfig", all_elements=settings, logger=None)
        cls.base_url = cls.testing_config.NonStandardElements.get("REMOTE_ADDRESS", t_Hello_remote.DEFAULT_ADDRESS)

        _level = logging.DEBUG if cls.testing_config.Verbose else logging.INFO
        Logger.InitializeLogger(level=_level, use_logfile=False)

    def test_get(self):
        _url = f"{self.base_url}/hello"
        try:
            result = TestRequest(url=_url, request="GET", params={}, logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            if result is not None:
                Logger.Log(f"Result: status '{result.status_code}', and data <{result.json()}>", logging.DEBUG)
            self.assertNotEqual(result, None)

    def test_post(self):
        _url = f"{self.base_url}/hello"
        try:
            result = TestRequest(url=_url, request="POST", params={}, logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            if result is not None:
                Logger.Log(f"Result: status '{result.status_code}', and data <{result.json()}>", logging.DEBUG)
            self.assertNotEqual(result, None)

    def test_put(self):
        _url = f"{self.base_url}/hello"
        Logger.Log(f"PUT test at {_url}", logging.DEBUG)
        try:
            result = TestRequest(url=_url, request="PUT", params={}, logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            if result:
                Logger.Log(f"Result: status '{result.status_code}', and data <{result.json()}>", logging.DEBUG)
            self.assertNotEqual(result, None)
