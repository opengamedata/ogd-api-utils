# import libraries
import json
import logging
from unittest import TestCase
# import 3rd-party libraries
from flask import Flask
# import ogd-core libraries.
from ogd.common.configs.TestConfig import TestConfig
from ogd.common.utils.Logger import Logger
Logger.InitializeLogger(level=logging.INFO, use_logfile=False)
# import locals
from src.ogd.apis.configs.ServerConfig import ServerConfig
from src.ogd.apis.HelloAPI import HelloAPI
from tests.config.t_config import settings

class LocalCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 1. Get testing config
        _testing_cfg = TestConfig.FromDict(name="HelloAPITestConfig", unparsed_elements=settings)

        _level       = logging.DEBUG if _testing_cfg.Verbose else logging.INFO
        _str_level   =       "DEBUG" if _testing_cfg.Verbose else "INFO"
        Logger.InitializeLogger(level=_level, use_logfile=False)

        # 2. Set up local Flask app to run tests
        cls.application = Flask(__name__)
        cls.application.logger.setLevel(_level)
        cls.application.secret_key = b'thisisafakesecretkey'

        # 3. Configure and register the HelloAPI with the local Flask app so we can test the Hello resource.
        _server_cfg_elems = {
            "API_VERSION" : "0.0.0-Testing",
            "DEBUG_LEVEL" : _str_level
        }
        _server_cfg = ServerConfig.FromDict(name="HelloAPITestServer", unparsed_elements=_server_cfg_elems)
        HelloAPI.register(app=cls.application, server_config=_server_cfg)

        cls.server = cls.application.test_client()

    def test_get(self):
        _url = "/hello"
        # 1. Run request
        result = self.server.get(_url)
        body = json.loads(result.get_data(as_text=True))
        # 2. Perform assertions
        self.assertIsNotNone(result, f"No response from {_url}")
        self.assertEqual(result.status, "200 OK", f"Bad status from {_url}")
        self.assertEqual(body.get("type"), "GET", f"Bad type from {_url}")
        self.assertIsNone(body.get("val"), f"Bad val from {_url}")
        self.assertEqual(body.get("msg"), "Hello! You GETted successfully!", f"Bad msg from {_url}")

    def test_post(self):
        _url = "/hello"
        # 1. Run request
        result = self.server.post(_url)
        body = json.loads(result.get_data(as_text=True))
        # 2. Perform assertions
        self.assertIsNotNone(result, f"No response from {_url}")
        self.assertEqual(result.status, "200 OK", f"Bad status from {_url}")
        self.assertEqual(body.get("type"), "POST", f"Bad type from {_url}")
        self.assertIsNone(body.get("val"), f"Bad val from {_url}")
        self.assertEqual(body.get("msg"), "Hello! You POSTed successfully!", f"Bad msg from {_url}")

    def test_put(self):
        _url = "/hello"
        # 1. Run request
        result = self.server.put(_url)
        body = json.loads(result.get_data(as_text=True))
        # 2. Perform assertions
        self.assertIsNotNone(result, f"No response from {_url}")
        self.assertEqual(result.status, "200 OK", f"Bad status from {_url}")
        self.assertEqual(body.get("type"), "PUT", f"Bad type from {_url}")
        self.assertIsNone(body.get("val"), f"Bad val from {_url}")
        self.assertEqual(body.get("msg"), "Hello! You PUTted successfully!", f"Bad msg from {_url}")
