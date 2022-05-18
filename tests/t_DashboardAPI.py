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
        t.test_get()

    class t_Dashboard:
        """Class for tests of Population
        """
        def __init__(self):
            """_summary_
            """
            self.TEST_PLAYER_ID = "ImmortanJoe"
            self.TEST_GAME      = "AQUALAB"

        def test_get(self):
            """_summary_
            """
            base = settings['EXTERN_SERVER']
            url = f"{base}/game/AQUALAB/metrics"
            print(f"GET test at {url}")
            params = {
                'start_datetime':datetime(year=2022, month=4, day=1).isoformat(),
                'end_datetime':datetime(year=2022, month=4, day=14).isoformat(),
                'metrics':'[ActiveJobs, SessionID, TopJobCompletionDestinations, TopJobSwitchDestinations]'
            }
            result = requests.get(url=url, params=params)
            if result is not None:
                print(f"Result of get:\n{result.text}")
            else:
                print(f"No response to GET request.")
