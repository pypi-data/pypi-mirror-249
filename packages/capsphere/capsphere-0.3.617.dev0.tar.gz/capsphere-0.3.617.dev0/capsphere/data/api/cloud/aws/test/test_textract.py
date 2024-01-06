# import unittest
#
# from capsphere.common.aws.textract import get_total_columns
# from capsphere.common.aws.test.data import AMBANK, MAYBANK, CIMB, CIMB_ISLAMIC, ALLIANCE, \
#     BANK_ISLAM, PUBLIC_BANK, HONG_LEONG
#
#
# class TestTextract(unittest.TestCase):
#
#     def test_get_total_columns(self):
#         self.assertEqual(get_total_columns(AMBANK), 6)
#         self.assertEqual(get_total_columns(MAYBANK), 5)
#         self.assertEqual(get_total_columns(CIMB), 6)
#         self.assertEqual(get_total_columns(CIMB_ISLAMIC), 6)
#         self.assertEqual(get_total_columns(ALLIANCE), 6)
#         self.assertEqual(get_total_columns(BANK_ISLAM), 6)
#         self.assertEqual(get_total_columns(PUBLIC_BANK), 5)
#         self.assertEqual(get_total_columns(HONG_LEONG), 5)
