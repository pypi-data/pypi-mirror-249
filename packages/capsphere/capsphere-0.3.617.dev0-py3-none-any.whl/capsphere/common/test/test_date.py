import unittest
from capsphere.common.date import modify_datestr


class TestDateFunctions(unittest.TestCase):

    def test_modify_datestr(self):
        date_to_test = '2022-12-04'
        date_in_future = modify_datestr(date_to_test, months=1)
        date_in_past = modify_datestr(date_to_test, months=-1)
        self.assertEqual('2023-01-04', date_in_future)
        self.assertEqual('2022-11-04', date_in_past)

# class TestConvertDate(unittest.TestCase):
#
#     date_format1 = '01Aug'
#     date_format2 = '01/08/2022'
#     date_format3 = '01/08'
#     date_format4 = '010822'
#     date_format5 = '101122'
#     date_format6 = '01-08-2022'
#
#     def test_convert_date(self):
#         date1 = convert_date(self.date_format1, "2022")
#         date2 = convert_date(self.date_format2)
#         date3 = convert_date(self.date_format3, "2022")
#         date4 = convert_date(self.date_format4)
#         date5 = convert_date(self.date_format5)
#         date6 = convert_date(self.date_format6)
#
#         self.assertEqual(date1, 'Aug 2022')
#         self.assertEqual(date2, 'Aug 2022')
#         self.assertEqual(date3, 'Aug 2022')
#         self.assertEqual(date4, 'Aug 2022')
#         self.assertEqual(date5, 'Nov 2022')
#         self.assertEqual(date6, 'Aug 2022')
