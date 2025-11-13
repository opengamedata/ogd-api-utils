# import libraries
import sys
import unittest
from pathlib import Path
from unittest import TestCase
# import ogd libraries
from ogd.common.configs.TestConfig import TestConfig
# import locals
from src.ogd.apis.utils.APIResponse import APIResponse
from tests.config.t_config import settings

_config = TestConfig.FromDict(name="APIResponseTestConfig", all_elements=settings)

@unittest.skip("No tests implemented yet")
class t_APIResponse(TestCase):
    @staticmethod
    def RunAll():
        pass

    @unittest.skip("Not yet implemented")
    def test_FromRequestResult(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_FromFromDict(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_Type(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_Value(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_Message(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_Status(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_AsDict(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_AsJSON(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_AsFlaskResponse(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_RequestErrored(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_ServerErrored(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_RequestSucceeded(self):
        pass

if __name__ == '__main__':
    unittest.main()
