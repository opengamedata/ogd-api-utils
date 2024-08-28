# import libraries
import requests
import unittest
from unittest import TestCase
# import ogd libraries.
from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
from ogd.apis.schemas.ServerConfigSchema import ServerConfigSchema
# import locals
from tests.config.t_config import settings

_config = TestConfigSchema.FromDict(name="HelloAPITestConfig", all_elements=settings, logger=None)

class t_HelloAPI:
    def RunAll(self):
        t = t_Hello()
        t.test_home()
        t.test_get()
        t.test_post()
        t.test_put()

# TODO : Set up class to spin up local HelloAPI app for testing.
@unittest.skip("Not set up to test directly, need to have a setup that spins up local HelloAPI instance.")
class t_Hello(TestCase):
    def test_home(self):
        _config.NonStandardElements.get('EXTERN_SERVER')
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
class t_ParamHello(TestCase):
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