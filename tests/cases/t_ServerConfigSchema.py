# import libraries
import unittest
from unittest import TestCase
# import locals
from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
from ogd.apis.schemas.ServerConfigSchema import ServerConfigSchema
from tests.config.t_config import settings

_config = TestConfigSchema.FromDict(name="APIUtilsTestConfig", all_elements=settings, logger=None)

@unittest.skip("No tests implemented yet")
class t_ServerConfigSchema(TestCase):
    @staticmethod
    def RunAll():
        pass

    def test_DebugLevel(self):
        pass

    def test_Version(self):
        pass

    def test_AsMarkdown(self):
        pass


if __name__ == '__main__':
    unittest.main()
