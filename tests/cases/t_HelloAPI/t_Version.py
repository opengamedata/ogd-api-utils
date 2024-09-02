# import libraries
import json
import logging
import requests
import unittest
from pathlib import Path
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

class t_Version_local(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 1. Get testing config
        _testing_cfg = TestConfigSchema.FromDict(name="HelloAPITestConfig", all_elements=settings, logger=None)
        _level     = logging.DEBUG if _testing_cfg.Verbose else logging.INFO
        _str_level =       "DEBUG" if _testing_cfg.Verbose else "INFO"
        Logger.std_logger.setLevel(_level)

        # 2. Set up local Flask app to run tests
        cls.application = Flask(__name__)
        cls.application.logger.setLevel(_level)
        cls.application.secret_key = b'thisisafakesecretkey'

        _server_cfg_elems = {
            "API_VERSION" : "0.0.0-Testing",
            "DEBUG_LEVEL" : _str_level
        }
        _server_cfg = ServerConfigSchema(name="HelloAPITestServer", all_elements=_server_cfg_elems, logger=cls.application.logger)
        HelloAPI.register(app=cls.application, server_config=_server_cfg)

        cls.server = cls.application.test_client()

    def test_get(self):
        _url = "/version"
        # 1. Run request
        Logger.Log(f"GET test at {_url}", logging.DEBUG)
        result = self.server.get(_url)
        Logger.Log(f"Result: status '{result.status}', and data <{result.data}>", logging.DEBUG)
        body = json.loads(result.get_data(as_text=True))
        # 2. Perform assertions
        self.assertNotEqual(result, None)
        self.assertEqual(result.status, "200 OK")
        self.assertEqual(body.get("type"), "GET")
        self.assertEqual(body.get("val"), '{"version":"0.0.0-Testing"}')
        self.assertEqual(body.get("msg"), "Successfully retrieved API version.")
        self.assertEqual(body.get("status"), "SUCCESS")

class t_Version_remote(TestCase):
    DEFAULT_ADDRESS = "127.0.0.1:5000"

    @classmethod
    def setUpClass(cls) -> None:
        testing_config = TestConfigSchema.FromDict(name="HelloAPITestConfig", all_elements=settings, logger=None)
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