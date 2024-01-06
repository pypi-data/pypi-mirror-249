import unittest

from pydantic import BaseModel
from datetime import datetime

from capsphere.data.db.helpers.utils import map_row_to_dataclass


class TestDataclassDate(BaseModel):
    time_key: str


class TestDataclassNodate(BaseModel):
    some_str: str
    some_int: int


class TestUtils(unittest.TestCase):

    def test_row_to_dataclass(self):
        row = (datetime.today(),)
        headers = ['time_key']
        actual = map_row_to_dataclass(TestDataclassDate, row, headers)
        self.assertEqual(str, type(actual.time_key))

    def test_row_to_dataclass_nodate(self):
        row = ('value', 25,)
        headers = ['some_str', 'some_int']
        actual = map_row_to_dataclass(TestDataclassNodate, row, headers)
        self.assertEqual(str, type(actual.some_str))
        self.assertEqual(int, type(actual.some_int))

    def test_row_to_dataclass_date(self):
        row = (datetime.today().date(),)
        headers = ['time_key']
        actual = map_row_to_dataclass(TestDataclassDate, row, headers)
        self.assertEqual(str, type(actual.time_key))
