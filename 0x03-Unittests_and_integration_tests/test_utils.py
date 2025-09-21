#!/usr/bin/env python3
from parameterized import parameterized
import unittest
import utils
from unittest.mock import Mock, patch

# class TestAccessNestedMap(unittest.TestCase):

    # @parameterized.expand([
    #     ({"a": 1}, ("a"), 1),
    #     ({"a": {"b": 2}}, ("a"), {'b':2}),
    #     ({"a": {"b": 2}}, ("a", "b"), 2)
    # ])
    # def test_access_nested_map(self, nested_map, path, expected_result):
    #     self.assertEqual(utils.access_nested_map(nested_map, path), expected_result)

    # @parameterized.expand([
    #     ({}, ('a'), KeyError),
    #     ({"a": 1}, ("a", "b"), KeyError)
    # ])
    # def test_access_nested_map_exception(self, nested_map, path, expected_result):
    #     with self.assertRaises(KeyError):
    #         utils.access_nested_map(nested_map, path), expected_result


class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload ):
        """ Test successful JSON retrieval from a remote URL"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch('utils.requests.get') as mock_get:
            mock.get.return_value = mock_response
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()