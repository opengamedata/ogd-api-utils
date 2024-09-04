# import libraries
import json
import logging
from unittest import TestCase
# import 3rd-party libraries
# import ogd-core libraries.
from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
from ogd.core.utils.Logger import Logger
# import locals
from src.ogd.apis.utils.TestRequest import TestRequest
from tests.config.t_config import settings

class t_ParamHello_remote(TestCase):
    DEFAULT_ADDRESS = "127.0.0.1:5000"

    @classmethod
    def setUpClass(cls) -> None:
        testing_config = TestConfigSchema.FromDict(name="HelloAPITestConfig", all_elements=settings, logger=None)
        cls.base_url = testing_config.NonStandardElements.get("REMOTE_ADDRESS", t_ParamHello_remote.DEFAULT_ADDRESS)
        cls.param = "Tester"

        _level = logging.DEBUG if testing_config.Verbose else logging.INFO
        Logger.std_logger.setLevel(_level)

    def test_get(self):
        _url = f"{self.base_url}/p_hello/{self.param}"
        try:
            result = TestRequest(url=_url, request="GET", params={}, logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None)
            self.assertEqual(result.status_code, 200)
            try:
                body = json.loads(result.text)
            except json.decoder.JSONDecodeError as err:
                Logger.Log(f"Could not parse json from {result.text}", logging.ERROR)
                body = {}
            self.assertEqual(body.get("type"), "GET")
            self.assertEqual(body.get("val"), "null")
            self.assertEqual(body.get("msg"), f"Hello {self.param}! You GETted successfully!")
            self.assertEqual(body.get("status"), "SUCCESS")

    def test_post(self):
        _url = f"{self.base_url}/p_hello/{self.param}"
        try:
            result = TestRequest(url=_url, request="POST", params={}, logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None)
            self.assertEqual(result.status_code, 200)
            try:
                body = json.loads(result.text)
            except json.decoder.JSONDecodeError as err:
                Logger.Log(f"Could not parse json from {result.text}", logging.ERROR)
                body = {}
            self.assertEqual(body.get("type"), "POST")
            self.assertEqual(body.get("val"), "null")
            self.assertEqual(body.get("msg"), "Hello! You POSTed successfully!")
            self.assertEqual(body.get("status"), "SUCCESS")

    def test_put(self):
        _url = f"{self.base_url}/hello"
        Logger.Log(f"PUT test at {_url}", logging.DEBUG)
        try:
            result = TestRequest(url=_url, request="PUT", params={}, logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None)
            self.assertEqual(result.status_code, 200)
            try:
                body = json.loads(result.text)
            except json.decoder.JSONDecodeError as err:
                Logger.Log(f"Could not parse json from {result.text}", logging.ERROR)
                body = {}
            self.assertEqual(body.get("type"), "PUT")
            self.assertEqual(body.get("val"), "null")
            self.assertEqual(body.get("msg"), "Hello! You PUTted successfully!")
            self.assertEqual(body.get("status"), "SUCCESS")
