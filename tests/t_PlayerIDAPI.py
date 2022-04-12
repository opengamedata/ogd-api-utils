# import libraries
import requests
from unittest import TestCase
# import locals
from tests.t_config import settings

class t_PlayerIDAPI(TestCase):
    """Testbed class for the PlayerID API.
    """
    def RunAll(self):
        t = t_PlayerIDAPI.t_Player()
        t.test_home()
        t.test_put()
        t.test_get()

    class t_Player:
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
            url = f"{base}/player/"
            print(f"GET test at {url}")
            result = requests.get(url=url)
            if result is not None:
                print(f"Result of get:\n{result.text}")
            else:
                print(f"No response to GET request.")

        def test_put(self):
            base = settings['EXTERN_SERVER']
            url = f"{base}/player/"
            print(f"POST test at {url}")
            params = { "player_id":"test_player", "name":"Test" }
            result = requests.put(url=url, params=params)
            if result is not None:
                print(f"Result of post:\n{result.text}")
            else:
                print(f"No response to POST request.")