# import libraries
import logging
import unittest
from unittest import TestCase
# import ogd libraries
from ogd.common.configs.TestConfig import TestConfig
from ogd.common.utils.Logger import Logger
# import locals
from ogd.apis.models.enums.RESTType import RESTType
from ogd.apis.models.APIRequest import APIRequest
from tests.config.t_config import settings


@unittest.skip("No tests implemented yet.")
class BasicInitCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _config = TestConfig.FromDict(name="APIResponseTestConfig", unparsed_elements=settings)
        _level = logging.DEBUG if _config.Verbose else logging.INFO
        Logger.InitializeLogger(level=_level, use_logfile=False)
        
    def setUp(self):
        self.request : APIRequest = APIRequest(url="ogd-services.fielddaylab.wisc.edu/apis/utils/main/app.wsgi/path/to/endpoint", request_type=RESTType.GET)

