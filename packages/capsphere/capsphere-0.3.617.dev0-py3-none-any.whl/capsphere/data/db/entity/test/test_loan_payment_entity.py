import unittest

from dotenv import load_dotenv

from capsphere.data.db import DbQueryService
from capsphere.data.db.connector.postgres import PostgresConnector
from capsphere.data.db.entity import LoanPaymentEntity
from capsphere.data.model.loan_payment import LoanPayment

load_dotenv()


@unittest.skip('Integration tests, skip for dev builds')
class TestLoanPaymentEntity(unittest.TestCase):
    db_query_service = DbQueryService(PostgresConnector())

    loan_payment_entity = LoanPaymentEntity(db_query_service)

    def test_get_by_loan_payment_ref_no(self):
        self.assertEqual(1, len(self.loan_payment_entity.get_by_loan_payment_ref_no('LPAY_183202262344BEA3B7CB')))
        # print(self.loan_payment_entity.get_by_loan_payment_ref_no('LPAY_183202262344BEA3B7CB'))

    def test_create(self):
        loan_payment = LoanPayment(loan_payment_ref_no='xxxxx', created_by_id=1813, updated_by_id=1813, loan_id=103)
        print(self.loan_payment_entity.create(loan_payment))

    def test_update(self):
        loan_payment = LoanPayment(loan_payment_ref_no='xxxxx', fpx_mode='FPXBRO')
        print(self.loan_payment_entity.update(loan_payment))
