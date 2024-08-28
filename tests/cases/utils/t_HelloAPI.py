# import libraries
import logging
import requests
import unittest
from multiprocessing import Process
from unittest import TestCase
# import 3rd-party libraries
from flask import Flask
# import ogd libraries.
from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
from ogd.core.utils.Logger import Logger
from ogd.apis.schemas.ServerConfigSchema import ServerConfigSchema
# import locals
from src.ogd.apis.schemas.ServerConfigSchema import ServerConfigSchema
from src.ogd.apis.HelloAPI import HelloAPI
from tests.config.t_config import settings

_config = TestConfigSchema.FromDict(name="HelloAPITestConfig", all_elements=settings, logger=None)

class t_HelloAPI:
    @staticmethod
    def RunAll(self):
        pass

# TODO : Set up class to spin up local HelloAPI app for testing.
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

        # cls.server = Process(target=cls.application.run, )
        # cls.server.start()
        cls.server = cls.application.test_client()

    @classmethod
    def tearDownClass(cls):
        pass
        # cls.server.terminate()
        # cls.server.join()

# if __name__ == '__main__':
# 	application.run(debug=True)

    def test_home(self):
        _config.NonStandardElements.get('EXTERN_SERVER')
        base = settings['EXTERN_SERVER']
        print(f"GET test at {base}")
        result = self.server.get(url=base)
        self.assertNotEqual(result, None)

    def test_get(self):
        base = settings['EXTERN_SERVER']
        url = f"{base}/hello"
        print(f"GET test at {url}")
        result = self.server.get(url=url)
        self.assertNotEqual(result, None)

    def test_post(self):
        base = settings['EXTERN_SERVER']
        url = f"{base}/hello"
        print(f"POST test at {url}")
        result = self.server.post(url=url)
        self.assertNotEqual(result, None)

    def test_put(self):
        base = settings['EXTERN_SERVER']
        url = f"{base}/hello"
        print(f"PUT test at {url}")
        result = self.server.put(url=url)
        self.assertNotEqual(result, None)

@unittest.skip("Not set up to test directly, need to have a setup that spins up local HelloAPI instance.")
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

@unittest.skip("Not set up to test directly, need to have a setup that spins up local HelloAPI instance.")
class t_Version(TestCase):
    def test_get(self):
        base = settings['EXTERN_SERVER']
        url = f"{base}/hello"
        print(f"GET test at {url}")
        result = requests.get(url=url)
        if result is not None:
            print(f"Result of get:\n{result.text}")
        else:
            print(f"No response to GET request.")