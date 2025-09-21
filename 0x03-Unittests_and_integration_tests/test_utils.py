#!/usr/bin/env python3
from parameterized import parameterized
import unittest
import utils

class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a"), 1),
        ({"a": {"b": 2}}, ("a"), {'b':2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])        

    def test_access_nested_map(self, access, nested_map, path, expected_result):
        self.assertEqual(utils.access_nested_map(nested_map, path), expected_result)

if __name__ = "__main__":
    unittest.main()