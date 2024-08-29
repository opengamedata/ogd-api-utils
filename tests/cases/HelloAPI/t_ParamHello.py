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

@unittest.skip("Not yet set up to test locally.")
class t_ParamHello_local(TestCase):
    def test_home(self):
        base = settings['EXTERN_SERVER']
        print(f"GET test at {base}")
        result = requests.get(url=base)
        if result is not None:
            print(f"Result of get:\n{result.text}")
        else:
            print(f"No response to GET request.")
        print()

    def test_get(self):
        base = settings['EXTERN_SERVER']
        url = f"{base}/hello"
        print(f"GET test at {url}")
        result = requests.get(url=url)
        if result is not None:
            print(f"Result of get:\n{result.text}")
        else:
            print(f"No response to GET request.")

    def test_post(self):
        base = settings['EXTERN_SERVER']
        url = f"{base}/hello"
        print(f"POST test at {url}")
        result = requests.post(url=url)
        if result is not None:
            print(f"Result of post:\n{result.text}")
        else:
            print(f"No response to POST request.")

    def test_put(self):
        base = settings['EXTERN_SERVER']
        url = f"{base}/hello"
        print(f"PUT test at {url}")
        result = requests.put(url=url)
        if result is not None:
            print(f"Result of put:\n{result.text}")
        else:
            print(f"No response to PUT request.")