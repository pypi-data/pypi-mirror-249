import unittest
from decimal import Decimal

from capsphere.data.model.loan_payment import LoanPayment


class TestDataRecord(unittest.TestCase):
    def test_loan_payment(self):
        loan_payment = LoanPayment()
        self.assertEqual(Decimal, type(loan_payment.to_dict()['loan_amount_paid']))
        self.assertEqual(str, type(loan_payment.to_json()))
