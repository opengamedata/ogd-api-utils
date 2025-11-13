# import libraries
import logging
import unittest
from unittest import TestCase
# import ogd libraries.
from ogd.common.configs.TestConfig import TestConfig
from ogd.common.models.SemanticVersion import SemanticVersion
from ogd.common.utils.Logger import Logger
# import locals
from src.ogd.apis.configs.ServerConfig import ServerConfig
from tests.config.t_config import settings

class t_ServerConfig(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 1. Get testing config
        _testing_cfg = TestConfig.FromDict(name="SchemaTestConfig", unparsed_elements=settings)
        _level     = logging.DEBUG if _testing_cfg.Verbose else logging.INFO
        Logger.std_logger.setLevel(_level)

        # 2. Set up local instance of class to test
        cls.test_schema = ServerConfig(
            name="Server Configuration",
            debug_level=logging.WARN,
            version=SemanticVersion(major=1, minor=2, patch=3, suffix="alpha"),
            other_elements={ "foo":"bar" }
        )

    @staticmethod
    def RunAll():
        pass

    def test_DebugLevel(self):
        _lvl = self.test_schema.DebugLevel
        self.assertIsInstance(_lvl, int)
        self.assertEqual(_lvl, logging.WARN)

    def test_Version(self):
        _ver = self.test_schema.Version
        self.assertIsInstance(_ver, SemanticVersion)
        self.assertEqual(_ver, SemanticVersion(1, 2, 3, "alpha"))

    @unittest.skip("Not yet implemented")
    def test_AsMarkdown(self):
        pass


if __name__ == '__main__':
    unittest.main()
