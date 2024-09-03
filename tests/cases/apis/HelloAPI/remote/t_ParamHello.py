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
# Logger.InitializeLogger(level=logging.INFO, use_logfile=False)
# import locals
try:
    from src.ogd.apis.schemas.ServerConfigSchema import ServerConfigSchema
    from src.ogd.apis.HelloAPI import HelloAPI
except ModuleNotFoundError as err:
    Logger.Log(f"Import error: {err}")
finally:
    from tests.config.t_config import settings

class t_ParamHello_remote(TestCase):
    DEFAULT_ADDRESS = "127.0.0.1:5000"

    @classmethod
    def setUpClass(cls) -> None:
        testing_config = TestConfigSchema.FromDict(name="HelloAPITestConfig", all_elements=settings, logger=None)
        cls.base_url = testing_config.NonStandardElements.get("REMOTE_ADDRESS", t_ParamHello_remote.DEFAULT_ADDRESS)

        _level = logging.DEBUG if testing_config.Verbose else logging.INFO
        Logger.std_logger.setLevel(_level)

    @unittest.skip("Not yet set up to test ParamHello remotely.")
    def test_get(self):
        param = "Tester"
        _url = f"{self.base_url}/p_hello/{param}"
        Logger.Log(f"GET test at {_url}", logging.DEBUG)
        try:
            result = requests.get(url=_url)
        except Exception as err:
            self.fail(str(err))
        else:
            Logger.Log(f"Result: status '{result.status_code}', and data <{result.json()}>", logging.DEBUG)
            self.assertNotEqual(result, None)

    @unittest.skip("Not yet set up to test ParamHello remotely.")
    def test_post(self):
        param = "Tester"
        _url = f"{self.base_url}/p_hello/{param}"
        Logger.Log(f"POST test at {_url}", logging.DEBUG)
        try:
            result = requests.post(url=_url)
        except Exception as err:
            self.fail(str(err))
        else:
            Logger.Log(f"Result: status '{result.status_code}', and data <{result.json()}>", logging.DEBUG)
            self.assertNotEqual(result, None)

    @unittest.skip("Not yet set up to test ParamHello remotely.")
    def test_put(self):
        param = "Tester"
        _url = f"{self.base_url}/p_hello/{param}"
        Logger.Log(f"PUT test at {_url}", logging.DEBUG)
        try:
            result = requests.put(url=_url)
        except Exception as err:
            self.fail(str(err))
        else:
            Logger.Log(f"Result: status '{result.status_code}', and data <{result.json()}>", logging.DEBUG)
            self.assertNotEqual(result, None)