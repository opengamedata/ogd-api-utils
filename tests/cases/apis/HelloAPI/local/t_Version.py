# import libraries
import json
import logging
from unittest import TestCase
# import 3rd-party libraries
from flask import Flask
# import ogd-core libraries.
from ogd.common.schemas.configs.TestConfigSchema import TestConfigSchema
from ogd.common.utils.Logger import Logger
Logger.InitializeLogger(level=logging.INFO, use_logfile=False)
# import locals
from src.ogd.apis.schemas.ServerConfigSchema import ServerConfigSchema
from src.ogd.apis.HelloAPI import HelloAPI
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
        _server_cfg = ServerConfigSchema.FromDict(name="HelloAPITestServer", all_elements=_server_cfg_elems, logger=cls.application.logger)
        HelloAPI.register(app=cls.application, server_config=_server_cfg)

        cls.server = cls.application.test_client()

    def test_get(self):
        _url = "/version"
        # 1. Run request
        self.application.logger.debug(f"GET test at {_url}")
        result = self.server.get(_url)
        self.application.logger.debug(f"Result: status '{result.status}', and data <{result.data}>")
        body = json.loads(result.get_data(as_text=True))
        # 2. Perform assertions
        self.assertNotEqual(result, None)
        self.assertEqual(result.status, "200 OK")
        self.assertEqual(body.get("type"), "GET")
        self.assertEqual(body.get("val"), '{"version": "0.0.0-Testing"}')
        self.assertEqual(body.get("msg"), "Successfully retrieved API version.")
        self.assertEqual(body.get("status"), "SUCCESS")
