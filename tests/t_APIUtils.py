# import libraries
import unittest
from unittest import TestCase
# import locals
from apis.APIUtils import parse_list, gen_interface
from tests.t_config import settings

class t_APIUtils(TestCase):
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

if __name__ == '__main__':
    unittest.main()
