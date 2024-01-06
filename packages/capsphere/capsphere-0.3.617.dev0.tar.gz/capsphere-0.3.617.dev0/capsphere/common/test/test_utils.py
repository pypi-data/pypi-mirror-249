import json
import unittest
from dataclasses import dataclass
from decimal import Decimal

from capsphere.common.utils import read_file, from_json

FILE_PATH = './mock_data.json'


@dataclass
class MockDataClass:
    some_key: str
    some_digits: Decimal
    digits_as_string: Decimal


class TestUtils(unittest.TestCase):

    def test_read(self):
        file = read_file(FILE_PATH)
        mock_dict = json.loads(file)
        self.assertEqual('some_value', mock_dict.get('some_key'))

    def test_serialize_as_decimal(self):
        data = read_file(FILE_PATH)
        mock_data_class = from_json(data, MockDataClass)
        self.assertEqual(MockDataClass, type(mock_data_class))
        self.assertEqual(Decimal, type(mock_data_class.some_digits))
        self.assertEqual(Decimal, type(mock_data_class.digits_as_string))
