# import libraries
import unittest
from unittest import TestCase
# import ogd libraries.
from ogd.common.schemas.configs.TestConfigSchema import TestConfigSchema
# import locals
from src.ogd.apis.schemas.ServerConfigSchema import ServerConfigSchema
from tests.config.t_config import settings

_config = TestConfigSchema.FromDict(name="ServerConfigSchemaTestConfig", all_elements=settings, logger=None)

@unittest.skip("No tests implemented yet")
class t_ServerConfigSchema(TestCase):
    @staticmethod
    def RunAll():
        pass

    @unittest.skip("Not yet implemented")
    def test_DebugLevel(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_Version(self):
        pass

    @unittest.skip("Not yet implemented")
    def test_AsMarkdown(self):
        pass


if __name__ == '__main__':
    unittest.main()
