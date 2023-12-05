# import libraries
import requests
from datetime import datetime
from unittest import TestCase
# import locals
from tests.t_config import settings

class t_DashboardAPI(TestCase):
    """Class containing tests of DashboardAPI
    """
    def RunAll(self):
        """_summary_
        """
        t = t_DashboardAPI.t_Dashboard()
        t.test_get_feature_list()
        t.test_post()

    class t_Dashboard:
        """Class for tests of Population
        """
        def __init__(self):
            """_summary_
            """
            self.TEST_PLAYER_ID = "ImmortanJoe"
            self.TEST_GAME      = "AQUALAB"

        def test_get_feature_list(self):
            """_summary_
            """
            base = settings['EXTERN_SERVER']
            url = f"{base}/populations/metrics/list/AQUALAB"
            print(f"GET test at {url}")
            result = requests.post(url=url)
            if result is not None:
                print(f"Result of get:\n{result.text}")
            else:
                print(f"No response to GET request.")

        def test_post(self):
            """_summary_
            """
            base = settings['EXTERN_SERVER']
            url = f"{base}/populations/metrics/"
            print(f"POST test at {url}")
            params = {
                'game_id':"AQUALAB",
                'start_datetime':datetime(year=2023, month=9, day=1).isoformat(),
                'end_datetime':datetime(year=2023, month=9, day=3).isoformat(),
                'metrics':'[ActiveJobs, SessionID, TopJobCompletionDestinations, TopJobSwitchDestinations]'
            }
            result = requests.post(url=url, params=params)
            if result is not None:
                print(f"Result of POST:\n{result.text}")
            else:
                print(f"No response to POST request.")
