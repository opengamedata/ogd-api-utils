# import libraries
import logging
import json
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
from src.ogd.apis.HelloAPI import HelloAPI
from tests.config.t_config import settings


class t_Hello_local(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 1. Get testing config
        cls.testing_config = TestConfigSchema.FromDict(name="HelloAPITestConfig", all_elements=settings, logger=None)

        # 2. Set up local Flask app to run tests
        cls.application = Flask(__name__)
        cls.application.logger.setLevel('DEBUG' if cls.testing_config.Verbose else 'INFO')
        cls.application.secret_key = b'thisisafakesecretkey'

        _cfg_elems = {
            "API_VERSION" : "0.0.0-Testing",
            "DEBUG_LEVEL" : "DEBUG"
        }
        _cfg = ServerConfigSchema(name="HelloAPITestServer", all_elements=_cfg_elems, logger=cls.application.logger)
        HelloAPI.register(app=cls.application, server_config=_cfg)

        cls.server = cls.application.test_client()

    def test_get(self):
        _url = "/hello"
        # 1. Run request
        self.application.logger.debug(f"GET test at {_url}")
        result = self.server.get(_url)
        self.application.logger.debug(f"Result: status '{result.status}', and data <{result.data}>")
        body = json.loads(result.get_data(as_text=True))
        # 2. Perform assertions
        self.assertNotEqual(result, None)
        self.assertEqual(result.status, "200 OK")
        self.assertEqual(body.get("type"), "GET")
        self.assertEqual(body.get("val"), "null")
        self.assertEqual(body.get("msg"), "Hello! You GETted successfully!")
        self.assertEqual(body.get("status"), "SUCCESS")

    def test_post(self):
        _url = f"/hello"
        # 1. Run request
        self.application.logger.debug(f"POST test at {_url}")
        result = self.server.post(_url)
        self.application.logger.debug(f"Result: status '{result.status}', and data <{result.data}>")
        body = json.loads(result.get_data(as_text=True))
        # 2. Perform assertions
        self.assertNotEqual(result, None)
        self.assertEqual(result.status, "200 OK")
        self.assertEqual(body.get("type"), "POST")
        self.assertEqual(body.get("val"), "null")
        self.assertEqual(body.get("msg"), "Hello! You POSTed successfully!")
        self.assertEqual(body.get("status"), "SUCCESS")

    def test_put(self):
        url = f"/hello"
        # 1. Run request
        self.application.logger.debug(f"PUT test at {url}")
        result = self.server.put(url)
        self.application.logger.debug(f"Result: status '{result.status}', and data <{result.data}>")
        body = json.loads(result.get_data(as_text=True))
        # 2. Perform assertions
        self.assertNotEqual(result, None)
        self.assertEqual(result.status, "200 OK")
        self.assertEqual(body.get("type"), "PUT")
        self.assertEqual(body.get("val"), "null")
        self.assertEqual(body.get("msg"), "Hello! You PUTted successfully!")
        self.assertEqual(body.get("status"), "SUCCESS")

class t_Hello_remote(TestCase):
    DEFAULT_ADDRESS = "127.0.0.1:5000"

    @classmethod
    def setUpClass(cls) -> None:
        testing_config = TestConfigSchema.FromDict(name="HelloAPITestConfig", all_elements=settings, logger=None)
        cls.base_url = testing_config.NonStandardElements.get("REMOTE_ADDRESS", t_Hello_remote.DEFAULT_ADDRESS)

        _level = logging.DEBUG if testing_config.Verbose else logging.INFO
        Logger.InitializeLogger(level=_level, use_logfile=False)

    @unittest.skip("Not yet set up to test Hello remotely.")
    def test_get(self):
        url = f"{self.base_url}/hello"
        Logger.Log(f"GET test at {url}", logging.DEBUG)
        try:
            result = requests.get(url=url)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None)

    @unittest.skip("Not yet set up to test Hello remotely.")
    def test_post(self):
        url = f"{self.base_url}/hello"
        Logger.Log(f"POST test at {url}", logging.DEBUG)
        try:
            result = requests.post(url=url)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None)

    @unittest.skip("Not yet set up to test Hello remotely.")
    def test_put(self):
        url = f"{self.base_url}/hello"
        Logger.Log(f"PUT test at {url}", logging.DEBUG)
        try:
            result = requests.put(url=url)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None)
