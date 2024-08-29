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

class t_Version(TestCase):
    @unittest.skip("Not set up to test version locally.")
    def test_get(self):
        base = settings['EXTERN_SERVER']
        url = f"{base}/hello"
        print(f"GET test at {url}")
        result = requests.get(url=url)
        if result is not None:
            print(f"Result of get:\n{result.text}")
        else:
            print(f"No response to GET request.")
