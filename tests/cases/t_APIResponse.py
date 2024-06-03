# import libraries
import unittest
from unittest import TestCase
# import locals
from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
from ogd.apis.utils.APIResponse import APIResponse
from tests.config.t_config import settings

_config = TestConfigSchema.FromDict(name="APIUtilsTestConfig", all_elements=settings, logger=None)

class t_APIResponse:
    @staticmethod
    def RunAll():
        pass

@unittest.skip("No tests implemented yet")
class t_ParseList(TestCase):
    def test_FromRequestResult(self):
        pass

    def test_FromFromDict(self):
        pass

    def test_Type(self):
        pass

    def test_Value(self):
        pass

    def test_Message(self):
        pass

    def test_Status(self):
        pass

    def test_AsDict(self):
        pass

    def test_AsJSON(self):
        pass

    def test_AsFlaskResponse(self):
        pass

    def test_RequestErrored(self):
        pass

    def test_ServerErrored(self):
        pass

    def test_RequestSucceeded(self):
        pass

if __name__ == '__main__':
    unittest.main()
