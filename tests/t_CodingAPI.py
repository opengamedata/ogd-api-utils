# import libraries
import requests
from unittest import TestCase
# import locals
from tests.t_config import settings

class t_CodingAPI(TestCase):
    def RunAll(self):
        t = t_CodingAPI.t_Coding()
        t.test_get()
        t.test_post()

    class t_Coding:
        def __init__(self):
            self.TEST_GAME      = "AQUALAB"
            self.TEST_PLAYER_ID = "ImmortanJoe"
            self.TEST_SESSION_ID = "1234567890"
            self.TEST_INDEX = "168"
            self.TEST_CODE = "SuccessfulPlay"

        def test_get(self):
            base = settings['EXTERN_SERVER']
            url = f"{base}/coding/game/{self.TEST_GAME}/codes"
            print(f"GET test at {url}")
            result = requests.get(url=url, params={})
            if result is not None:
                print(f"Result of get:\n{result.text}")
            else:
                print(f"No response to GET request.")

        def test_post(self):
            base = settings['EXTERN_SERVER']
            url = f"{base}/game/{self.TEST_GAME}/player/{self.TEST_PLAYER_ID}/session/{self.TEST_SESSION_ID}/index/{self.TEST_INDEX}/code/{self.TEST_CODE}"
            print(f"POST test at {url}")
            params = { 'coder':"Luke", "notes":"This is a note!" }
            result = requests.post(url=url, params=params)
            if result is not None:
                print(f"Result of post:\n{result.text}")
            else:
                print(f"No response to POST request.")