# import libraries
import logging
import unittest
from unittest import TestCase
# import ogd libraries.
from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
from ogd.core.utils.Logger import Logger
# import locals
try:
    from src.ogd.apis.utils.APIUtils import parse_list, gen_interface
except ModuleNotFoundError as err:
    Logger.Log(f"Import error: {err}")
finally:
    from tests.config.t_config import settings

class t_ParseList(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _config = TestConfigSchema.FromDict(name="APIUtilsTestConfig", all_elements=settings, logger=None)
        _level = logging.DEBUG if _config.Verbose else logging.INFO
        Logger.InitializeLogger(level=_level, use_logfile=False)

    def test_parse_list_empty(self):
        list_str = "[]"
        parsed = parse_list(list_str=list_str, logger=Logger.std_logger)
        self.assertEqual(parsed, None)

    def test_parse_list_one_elem(self):
        list_str = '["FeatureName"]'
        parsed = parse_list(list_str=list_str, logger=Logger.std_logger)
        self.assertEqual(parsed, ["FeatureName"])

    def test_parse_list_three_elem(self):
        list_str = '["FeatureName1", "FeatureName2", "FeatureName3"]'
        parsed = parse_list(list_str=list_str, logger=Logger.std_logger)
        self.assertEqual(parsed, ["FeatureName1", "FeatureName2", "FeatureName3"])

    def test_parse_list_invalid(self):
        list_str = "Not a [list] type of thing"
        parsed = parse_list(list_str=list_str, logger=Logger.std_logger)
        self.assertEqual(parsed, None)

class t_GenInterface(TestCase):
    @unittest.skip("No tests written yet")
    def test_gen_anything(self):
        pass

if __name__ == '__main__':
    unittest.main()
