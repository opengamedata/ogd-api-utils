# import libraries
import sys
import unittest
from pathlib import Path
from unittest import TestCase
# import ogd libraries
from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
# import locals
from src.ogd.apis.utils.APIResponse import APIResponse
from tests.config.t_config import settings

_config = TestConfigSchema.FromDict(name="APIResponseTestConfig", all_elements=settings, logger=None)

@unittest.skip("No tests implemented yet")
class t_APIResponse(TestCase):
    @staticmethod
    def RunAll():
        pass

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
