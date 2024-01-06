import unittest

from dotenv import load_dotenv

from capsphere.data.db import DbQueryService
from capsphere.data.db.connector.postgres import PostgresConnector
from capsphere.data.db.entity import LoanPaymentEntity
from capsphere.service.loan_payment_creator import LoanPaymentCreator
from capsphere.service.test.test_data import LOAN_PAYMENT_DICT

load_dotenv()


class TestLoanPaymentCreator(unittest.TestCase):
    loan_payment_entity = LoanPaymentEntity(DbQueryService(PostgresConnector()))

    def test_create_loan_payment(self):
        loan_payment_creator = LoanPaymentCreator(LOAN_PAYMENT_DICT, self.loan_payment_entity)
        loan_payment_creator.process()
        self.assertEqual(1, len(self.loan_payment_entity.get_by_loan_payment_ref_no(LOAN_PAYMENT_DICT['loan_payment_ref_no'])))