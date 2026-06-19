# import libraries
import logging
from unittest import TestCase
# import ogd-core libraries.
from ogd.common.configs.TestConfig import TestConfig
from ogd.common.utils.Logger import Logger
from ogd.apis.models.APIRequest import APIRequest
# import locals
from tests.config.t_config import settings

class RemoteCase(TestCase):
    DEFAULT_ADDRESS = "127.0.0.1:5000"

    @classmethod
    def setUpClass(cls) -> None:
        testing_config = TestConfig.FromDict(name="HelloAPITestConfig", unparsed_elements=settings)
        cls.base_url = testing_config.NonStandardElements.get("REMOTE_ADDRESS", RemoteCase.DEFAULT_ADDRESS)
        cls.param = "Tester"

        _level = logging.DEBUG if testing_config.Verbose else logging.INFO
        Logger.InitializeLogger(level=_level, use_logfile=False)

    def test_get(self):
        _url = f"{self.base_url}/p_hello/{self.param}"
        try:
            response = APIRequest(url=_url, request_type="GET", params={}).Execute(logger=Logger.std_logger)
        except Exception as err: # pylint: disable=broad-exception-caught
            self.fail(str(err))
        else:
            self.assertIsNotNone(response, f"No response from {_url}")
            self.assertTrue(response.OK, f"Bad status from {_url}: {response.Status}")
            self.assertEqual(str(response.Type), "GET", f"Bad type from {_url}")
            self.assertIsNone(response.Value, f"Bad val from {_url}")
            self.assertEqual(response.Message, f"Hello {self.param}! You GETted successfully!", f"Bad msg from {_url}")

    def test_post(self):
        _url = f"{self.base_url}/p_hello/{self.param}"
        try:
            response = APIRequest(url=_url, request_type="POST", params={}).Execute(logger=Logger.std_logger)
        except Exception as err: # pylint: disable=broad-exception-caught
            self.fail(str(err))
        else:
            self.assertIsNotNone(response, f"No response from {_url}")
            self.assertTrue(response.OK, f"Bad status from {_url}: {response.Status}")
            self.assertEqual(str(response.Type), "POST", f"Bad type from {_url}")
            self.assertIsNone(response.Value, f"Bad val from {_url}")
            self.assertEqual(response.Message, f"Hello {self.param}! You POSTed successfully!", f"Bad msg from {_url}")

    def test_put(self):
        _url = f"{self.base_url}/p_hello/{self.param}"
        Logger.Log(f"PUT test at {_url}", logging.DEBUG)
        try:
            response = APIRequest(url=_url, request_type="PUT", params={}).Execute(logger=Logger.std_logger)
        except Exception as err: # pylint: disable=broad-exception-caught
            self.fail(str(err))
        else:
            self.assertIsNotNone(response, f"No response from {_url}")
            self.assertTrue(response.OK, f"Bad status from {_url}: {response.Status}")
            self.assertEqual(str(response.Type), "PUT", f"Bad type from {_url}")
            self.assertIsNone(response.Value, f"Bad val from {_url}")
            self.assertEqual(response.Message, f"Hello {self.param}! You PUTted successfully!", f"Bad msg from {_url}")
