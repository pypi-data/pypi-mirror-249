# import unittest
#
# from unittest import mock
# from unittest.mock import Mock
# from capsphere.common.aws.s3 import get_env_vars
#
#
# class TestS3(unittest.TestCase):
#
#     @mock.patch('builtins.open')
#     @mock.patch('json.load')
#     def test_get_env(self, mock_json_load, mock_open):
#         mock_data = {'key': 'value'}
#         mock_file = mock.Mock()
#         mock_open.return_value.__enter__.return_value = mock_file
#         mock_json_load.return_value = mock_data
#
#         result = get_env_vars()
#
#         mock_open.assert_called_once_with('./config.json')
#         mock_json_load.assert_called_once_with(mock_file)
#         self.assertEqual(result, mock_data)
#
#     def test_get_total_objects(self):
#         pass
#
#     def test_delete_s3_objects(self):
#         pass

