# import libraries
import logging
from unittest import TestCase
# import 3rd-party libraries
# import ogd-core libraries.
from ogd.common.configs.TestConfig import TestConfig
from ogd.common.utils.Logger import Logger
# import locals
from ogd.apis.models.APIRequest import APIRequest
from tests.config.t_config import settings

class t_Hello_remote(TestCase):
    DEFAULT_ADDRESS = "127.0.0.1:5000"

    @classmethod
    def setUpClass(cls) -> None:
        cls.testing_config = TestConfig.FromDict(name="HelloAPITestConfig", unparsed_elements=settings)
        cls.base_url = cls.testing_config.NonStandardElements.get("REMOTE_ADDRESS", t_Hello_remote.DEFAULT_ADDRESS)

        _level = logging.DEBUG if cls.testing_config.Verbose else logging.INFO
        Logger.InitializeLogger(level=_level, use_logfile=False)

    def test_get(self):
        _url = f"{self.base_url}/hello"
        try:
            result = APIRequest(url=_url, request_type="GET", params={}).Execute(logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None, f"No response from {_url}")
            self.assertEqual(result.Status.value, 200, f"Bad status from {_url}")
            self.assertEqual(str(result.Type), "GET", f"Bad type from {_url}")
            self.assertEqual(result.Value, None, f"Bad val from {_url}")
            self.assertEqual(result.Message, "Hello! You GETted successfully!", f"Bad msg from {_url}")

    def test_post(self):
        _url = f"{self.base_url}/hello"
        try:
            result = APIRequest(url=_url, request_type="POST", params={}).Execute(logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None, f"No response from {_url}")
            self.assertEqual(result.Status.value, 200, f"Bad status from {_url}")
            self.assertEqual(str(result.Type), "POST", f"Bad type from {_url}")
            self.assertEqual(result.Value, None, f"Bad val from {_url}")
            self.assertEqual(result.Message, "Hello! You POSTed successfully!", f"Bad msg from {_url}")

    def test_put(self):
        _url = f"{self.base_url}/hello"
        Logger.Log(f"PUT test at {_url}", logging.DEBUG)
        try:
            result = APIRequest(url=_url, request_type="PUT", params={}).Execute(logger=Logger.std_logger)
        except Exception as err:
            self.fail(str(err))
        else:
            self.assertNotEqual(result, None, f"No response from {_url}")
            self.assertEqual(result.Status.value, 200, f"Bad status from {_url}")
            self.assertEqual(str(result.Type), "PUT", f"Bad type from {_url}")
            self.assertEqual(result.Value, None, f"Bad val from {_url}")
            self.assertEqual(result.Message, "Hello! You PUTted successfully!", f"Bad msg from {_url}")
