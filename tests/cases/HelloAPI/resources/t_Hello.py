# import libraries
import logging
import requests
import unittest
from multiprocessing import Process
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

_config = TestConfigSchema.FromDict(name="HelloAPITestConfig", all_elements=settings, logger=None)

class t_Hello_local(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Logger.InitializeLogger(level=logging.INFO, use_logfile=False)
        cls.application = Flask(__name__)
        cls.application.logger.setLevel('DEBUG')
        cls.application.secret_key = b'thisisafakesecretkey'

        _cfg_elems = {
            "API_VERSION" : "0.0.0-Testing",
            "DEBUG_LEVEL" : "DEBUG"
        }
        _cfg = ServerConfigSchema(name="HelloAPITestServer", all_elements=_cfg_elems, logger=cls.application.logger)
        HelloAPI.register(app=cls.application, server_config=_cfg)

        cls.server = cls.application.test_client()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get(self):
        _url = "/hello"
        Logger.Log(f"GET test at {_url}")
        result = self.server.get(_url)
        self.assertNotEqual(result, None)
        self.assertEqual(result.status, "200 OK")
        Logger.Log(f"Result: {result}, with status '{result.status}', and data <{result.data}>")

    def test_post(self):
        _url = f"/hello"
        Logger.Log(f"POST test at {_url}")
        result = self.server.post(_url)
        self.assertNotEqual(result, None)
        Logger.Log(f"Result: {result}")

    def test_put(self):
        url = f"/hello"
        Logger.Log(f"PUT test at {url}")
        result = self.server.put(url)
        self.assertNotEqual(result, None)
        Logger.Log(f"Result: {result}")

class t_Hello_remote(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Logger.InitializeLogger(level=logging.INFO, use_logfile=False)
        cls.application = Flask(__name__)
        cls.application.logger.setLevel('DEBUG')
        cls.application.secret_key = b'thisisafakesecretkey'

        _cfg_elems = {
            "API_VERSION" : "0.0.0-Testing",
            "DEBUG_LEVEL" : "DEBUG"
        }
        _cfg = ServerConfigSchema(name="HelloAPITestServer", all_elements=_cfg_elems, logger=cls.application.logger)
        HelloAPI.register(app=cls.application, server_config=_cfg)

        cls.server = cls.application.test_client()

    @classmethod
    def tearDownClass(cls):
        pass

    @unittest.skip("Not yet set up to test Hello remote deploy.")
    def test_home(self):
        _config.NonStandardElements.get('EXTERN_SERVER')
        base = settings['EXTERN_SERVER']
        print(f"GET test at {base}")
        result = self.server.get(url=base)
        self.assertNotEqual(result, None)

    @unittest.skip("Not yet set up to test Hello remote deploy.")
    def test_get(self):
        base = settings['EXTERN_SERVER']
        url = f"{base}/hello"
        print(f"GET test at {url}")
        result = self.server.get(url=url)
        self.assertNotEqual(result, None)

    @unittest.skip("Not yet set up to test Hello remote deploy.")
    def test_post(self):
        base = settings['EXTERN_SERVER']
        url = f"{base}/hello"
        print(f"POST test at {url}")
        result = self.server.post(url=url)
        self.assertNotEqual(result, None)

    @unittest.skip("Not yet set up to test Hello remote deploy.")
    def test_put(self):
        base = settings['EXTERN_SERVER']
        url = f"{base}/hello"
        print(f"PUT test at {url}")
        result = self.server.put(url=url)
        self.assertNotEqual(result, None)
