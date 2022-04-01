# import libraries
import requests
from unittest import TestCase
# import locals
from tests.t_config import settings

class t_GameStateAPI(TestCase):
    def RunAll(self):
        t = t_GameStateAPI.t_GameState()
        t.test_home()
        t.test_get()
        t.test_get_multi()
        t.test_post()

    class t_GameState:
        def __init__(self):
            self.TEST_PLAYER_ID = "ImmortanJoe"
            self.TEST_GAME      = "AQUALAB"

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
            url = f"{base}/player/{self.TEST_PLAYER_ID}/game/{self.TEST_GAME}/state"
            print(f"GET test at {url}")
            params = { 'count':1, 'offset':0 }
            result = requests.get(url=url, params=params)
            if result is not None:
                print(f"Result of get:\n{result.text}")
            else:
                print(f"No response to GET request.")

        def test_get_multi(self):
            base = settings['EXTERN_SERVER']
            url = f"{base}/player/{self.TEST_PLAYER_ID}/game/{self.TEST_GAME}/state"
            print(f"GET test at {url}")
            params = { 'count':3, 'offset':0 }
            result = requests.get(url=url, params=params)
            if result is not None:
                print(f"Result of get:\n{result.text}")
            else:
                print(f"No response to GET request.")

        def test_post(self):
            base = settings['EXTERN_SERVER']
            url = f"{base}/player/{self.TEST_PLAYER_ID}/game/{self.TEST_GAME}/state"
            print(f"POST test at {url}")
            params = { 'state':"{'data':'test data'}" }
            result = requests.post(url=url, params=params)
            if result is not None:
                print(f"Result of post:\n{result.text}")
            else:
                print(f"No response to POST request.")