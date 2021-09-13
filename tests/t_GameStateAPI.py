# global imports
import requests
from unittest import TestCase
# local imports
from tests.t_config import settings

class t_GameStateAPI(TestCase):
    def RunAll(self):
        t = t_GameStateAPI.t_GameState()
        t.test_post()
        t.test_get()

    class t_GameState:
        def __init__(self):
            self.TEST_PLAYER_ID = "test_player"
            self.TEST_GAME      = "AQUALAB"

        def test_get(self):
            base = settings['EXTERN_SERVER']
            url = f"{base}/player/{self.TEST_PLAYER_ID}/game/{self.TEST_GAME}/state"
            params = { 'count':1, 'offset':0 }
            result = requests.get(url=url, params=params).json()
            print(f"result of get:\n{result}")

        def test_post(self):
            base = settings['EXTERN_SERVER']
            url = f"{base}/player/{self.TEST_PLAYER_ID}/game/{self.TEST_GAME}/state"
            params = { 'state':"{'data':'test data'}" }
            result = requests.post(url=url, params=params).json()
            print(f"result of post:\n{result}")