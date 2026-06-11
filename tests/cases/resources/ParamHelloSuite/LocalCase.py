# import libraries
import logging
from json.decoder import JSONDecodeError
from unittest import TestCase
# import 3rd-party libraries
from flask import Flask
# import ogd-core libraries.
from ogd.apis.models.APIResponse import APIResponse, ResponseStatus
from ogd.apis.models.enums.RESTType import RESTType
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
        _server_cfg = ServerConfig.FromDict(name="HelloAPITestServer", unparsed_elements=_server_cfg_elems)
        HelloAPI.register(app=cls.application, server_config=_server_cfg)

        cls.server = cls.application.test_client()

    def test_get(self):
        param = "Tester"
        _url = f"/p_hello/{param}"
        # 1. Run request
        raw_response = self.server.get(_url)
        try:
            response = APIResponse.FromDict(all_elements=raw_response.json or {}, status=ResponseStatus(raw_response.status_code))
        except JSONDecodeError as err:
            self.fail(f"Could not parse {raw_response.text} to JSON!\n{err}")
        raw_response.close()
        # 2. Perform assertions
        self.assertIsNotNone(response, f"No response from {_url}")
        if response:
            self.assertTrue(response.OK, f"Bad status from {_url}")
            self.assertEqual(response.Type, RESTType.GET, f"Bad type from {_url}")
            self.assertIsNone(response.Value, f"Bad val from {_url}")
            self.assertEqual(response.Message, f"Hello {param}! You GETted successfully!", f"Bad msg from {_url}")

    def test_post(self):
        param = "Tester"
        _url = f"/p_hello/{param}"
        # 1. Run request
        raw_response = self.server.post(_url)
        try:
            response = APIResponse.FromDict(all_elements=raw_response.json or {}, status=ResponseStatus(raw_response.status_code))
        except JSONDecodeError as err:
            self.fail(f"Could not parse {raw_response.text} to JSON!\n{err}")
        raw_response.close()
        # 2. Perform assertions
        self.assertIsNotNone(response, f"No response from {_url}")
        if response:
            self.assertTrue(response.OK, f"Bad status from {_url}")
            self.assertEqual(response.Type, RESTType.POST, f"Bad type from {_url}")
            self.assertIsNone(response.Value, f"Bad val from {_url}")
            self.assertEqual(response.Message, f"Hello {param}! You POSTed successfully!", f"Bad msg from {_url}")

    def test_put(self):
        param = "Tester"
        _url = f"/p_hello/{param}"
        # 1. Run request
        raw_response = self.server.put(_url)
        try:
            response = APIResponse.FromDict(all_elements=raw_response.json or {}, status=ResponseStatus(raw_response.status_code))
        except JSONDecodeError as err:
            self.fail(f"Could not parse {raw_response.text} to JSON!\n{err}")
        raw_response.close()
        # 2. Perform assertions
        self.assertIsNotNone(response, f"No response from {_url}")
        if response:
            self.assertTrue(response.OK, f"Bad status from {_url}")
            self.assertEqual(response.Type, RESTType.PUT, f"Bad type from {_url}")
            self.assertIsNone(response.Value, f"Bad val from {_url}")
            self.assertEqual(response.Message, f"Hello {param}! You PUTted successfully!", f"Bad msg from {_url}")
