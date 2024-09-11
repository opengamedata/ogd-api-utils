# import libraries
import json
import logging
from unittest import TestCase
# import 3rd-party libraries
# import ogd-core libraries.
from ogd.common.schemas.configs.TestConfigSchema import TestConfigSchema
from ogd.common.utils.Logger import Logger
# import locals
from src.ogd.apis.utils.TestRequest import TestRequest
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
            self.assertNotEqual(result, None)
            self.assertEqual(result.status_code, 200)
            try:
                body = json.loads(result.text)
            except json.decoder.JSONDecodeError as err:
                Logger.Log(f"Could not parse json from {result.text}", logging.ERROR)
                body = {}
            self.assertEqual(body.get("type"), "GET")
            self.assertEqual(body.get("val"), "null")
            self.assertEqual(body.get("msg"), "Hello! You GETted successfully!")
            self.assertEqual(body.get("status"), "SUCCESS")

    def test_post(self):
        _url = f"{self.base_url}/hello"
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
