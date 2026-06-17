# import libraries
import logging
from unittest import TestCase
# import 3rd-party libraries
# import ogd-core libraries.
from ogd.common.configs.TestConfig import TestConfig
from ogd.common.utils.Logger import Logger
from ogd.apis.models.APIRequest import APIRequest
from ogd.apis.models.APIResponse import APIResponse
# import locals
from tests.config import t_config

class RemoteCase(TestCase):
    DEFAULT_ADDRESS = "127.0.0.1:5000"

    @classmethod
    def setUpClass(cls) -> None:
        cls.testing_config = TestConfig.FromDict(name="HelloAPITestConfig", unparsed_elements=t_config.settings)
        cls.base_url = cls.testing_config.NonStandardElements.get("REMOTE_ADDRESS", RemoteCase.DEFAULT_ADDRESS)

        _level = logging.DEBUG if cls.testing_config.Verbose else logging.INFO
        Logger.InitializeLogger(level=_level, use_logfile=False)

    def test_get(self):
        _url = f"{self.base_url}/hello"
        try:
            response : APIResponse = APIRequest(url=_url, request_type="GET", params={}).Execute(logger=Logger.std_logger)
        except Exception as err: # pylint: disable=broad-exception-caught
            self.fail(str(err))
        else:
            self.assertIsNotNone(response, f"No response from {_url}")
            self.assertTrue(response.OK, f"Bad status from {_url}: {response.Status}")
            self.assertEqual(str(response.Type), "GET", f"Bad type from {_url}")
            self.assertIsNone(response.Value, f"Bad val from {_url}")
            self.assertEqual(response.Message, "Hello! You GETted successfully!", f"Bad msg from {_url}")

    def test_post(self):
        _url = f"{self.base_url}/hello"
        try:
            response : APIResponse = APIRequest(url=_url, request_type="POST", params={}).Execute(logger=Logger.std_logger)
        except Exception as err: # pylint: disable=broad-exception-caught
            self.fail(str(err))
        else:
            self.assertIsNotNone(response, f"No response from {_url}")
            self.assertTrue(response.OK, f"Bad status from {_url}: {response.Status}")
            self.assertEqual(str(response.Type), "POST", f"Bad type from {_url}")
            self.assertIsNone(response.Value, f"Bad val from {_url}")
            self.assertEqual(response.Message, "Hello! You POSTed successfully!", f"Bad msg from {_url}")

    def test_put(self):
        _url = f"{self.base_url}/hello"
        Logger.Log(f"PUT test at {_url}", logging.DEBUG)
        try:
            response : APIResponse = APIRequest(url=_url, request_type="PUT", params={}).Execute(logger=Logger.std_logger)
        except Exception as err: # pylint: disable=broad-exception-caught
            self.fail(str(err))
        else:
            self.assertIsNotNone(response, f"No response from {_url}")
            self.assertTrue(response.OK, f"Bad status from {_url}: {response.Status}")
            self.assertEqual(str(response.Type), "PUT", f"Bad type from {_url}")
            self.assertIsNone(response.Value, f"Bad val from {_url}")
            self.assertEqual(response.Message, "Hello! You PUTted successfully!", f"Bad msg from {_url}")
