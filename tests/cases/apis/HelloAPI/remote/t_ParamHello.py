# import libraries
import json
import logging
from unittest import TestCase
# import 3rd-party libraries
# import ogd-core libraries.
from ogd.common.configs.TestConfig import TestConfig
from ogd.common.utils.Logger import Logger
# import locals
from src.ogd.apis.utils.TestRequest import APIRequest
from tests.config.t_config import settings

class t_ParamHello_remote(TestCase):
    DEFAULT_ADDRESS = "127.0.0.1:5000"

    @classmethod
    def setUpClass(cls) -> None:
        testing_config = TestConfig.FromDict(name="HelloAPITestConfig", unparsed_elements=settings)
        cls.base_url = testing_config.NonStandardElements.get("REMOTE_ADDRESS", t_ParamHello_remote.DEFAULT_ADDRESS)
        cls.param = "Tester"

        _level = logging.DEBUG if testing_config.Verbose else logging.INFO
        Logger.std_logger.setLevel(_level)

    def test_get(self):
        _url = f"{self.base_url}/p_hello/{self.param}"
        try:
            result = APIRequest(url=_url, request="GET", params={}, logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None, f"No response from {_url}")
            self.assertEqual(result.status_code, 200, f"Bad status from {_url}")
            try:
                body = json.loads(result.text)
            except json.decoder.JSONDecodeError:
                Logger.Log(f"Could not parse json result '{result.text}' from {_url}", logging.ERROR)
                body = {}
            self.assertEqual(body.get("type"), "GET", f"Bad type from {_url}")
            self.assertEqual(body.get("val"), None, f"Bad val from {_url}")
            self.assertEqual(body.get("msg"), f"Hello {self.param}! You GETted successfully!", f"Bad msg from {_url}")

    def test_post(self):
        _url = f"{self.base_url}/p_hello/{self.param}"
        try:
            result = APIRequest(url=_url, request="POST", params={}, logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None, f"No response from {_url}")
            self.assertEqual(result.status_code, 200, f"Bad status from {_url}")
            try:
                body = json.loads(result.text)
            except json.decoder.JSONDecodeError:
                Logger.Log(f"Could not parse json result '{result.text}' from {_url}", logging.ERROR)
                body = {}
            self.assertEqual(body.get("type"), "POST", f"Bad type from {_url}")
            self.assertEqual(body.get("val"), None, f"Bad val from {_url}")
            self.assertEqual(body.get("msg"), f"Hello {self.param}! You POSTed successfully!", f"Bad msg from {_url}")

    def test_put(self):
        _url = f"{self.base_url}/p_hello/{self.param}"
        Logger.Log(f"PUT test at {_url}", logging.DEBUG)
        try:
            result = APIRequest(url=_url, request="PUT", params={}, logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None, f"No response from {_url}")
            self.assertEqual(result.status_code, 200, f"Bad status from {_url}")
            try:
                body = json.loads(result.text)
            except json.decoder.JSONDecodeError:
                Logger.Log(f"Could not parse json result '{result.text}' from {_url}", logging.ERROR)
                body = {}
            self.assertEqual(body.get("type"), "PUT", f"Bad type from {_url}")
            self.assertEqual(body.get("val"), None, f"Bad val from {_url}")
            self.assertEqual(body.get("msg"), f"Hello {self.param}! You PUTted successfully!", f"Bad msg from {_url}")
