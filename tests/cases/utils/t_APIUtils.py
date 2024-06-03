# import libraries
import unittest
from unittest import TestCase
# import ogd libraries.
from ogd.core.schemas.configs.TestConfigSchema import TestConfigSchema
# import locals
from src.ogd.apis.utils.APIUtils import parse_list, gen_interface
from tests.config.t_config import settings

_config = TestConfigSchema.FromDict(name="APIUtilsTestConfig", all_elements=settings, logger=None)

class t_APIUtils:
    @staticmethod
    def RunAll():
        pass

class t_ParseList(TestCase):
    def test_parse_list_empty(self):
        list_str = "[]"
        parsed = parse_list(list_str=list_str)
        self.assertEqual(parsed, [])

    def test_parse_list_one_elem(self):
        list_str = "[FeatureName]"
        parsed = parse_list(list_str=list_str)
        self.assertEqual(parsed, ["FeatureName"])

    def test_parse_list_three_elem(self):
        list_str = "[FeatureName1, FeatureName2, FeatureName3]"
        parsed = parse_list(list_str=list_str)
        self.assertEqual(parsed, ["FeatureName1, FeatureName2, FeatureName3"])

    def test_parse_list_invalid(self):
        list_str = "Not a [list] type of thing"
        parsed = parse_list(list_str=list_str)
        self.assertEqual(parsed, None)

@unittest.skip("No tests written yet")
class t_GenInterface(TestCase):
    def test_gen_anything(self):
        pass

if __name__ == '__main__':
    unittest.main()
