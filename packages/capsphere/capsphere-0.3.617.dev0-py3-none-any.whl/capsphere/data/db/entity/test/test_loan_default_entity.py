import logging
import os
import unittest
from decimal import Decimal

from dotenv import load_dotenv

from capsphere.data.db import DbQueryService
from capsphere.data.db.connector.postgres import PostgresConnector
from capsphere.data.db.entity import LoanDefaultEntity
from capsphere.data.db.entity.test.db_setup import run_sql_script, drop_table

load_dotenv()

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class TestLoanDefaultEntity(unittest.TestCase):
    db_query_service = DbQueryService(PostgresConnector())

    loan_default_entity = LoanDefaultEntity(db_query_service)

    @classmethod
    def setUpClass(cls):
        # try:
        logger.info('Creating and inserting data for loan_defaults tables...')
        run_sql_script('scripts/loan_defaults.sql')
        logger.info('Running tests for loan_defaults...')
        # except Exception as e:
        #     logger.error(f'setup error:{e}. Running tearDownClass')
        #     cls.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        logger.info('Dropping tables...')
        try:
            if cls.db_query_service:
                drop_table('loan_defaults')
            logger.info('Dropped loan_defaults table')
        except Exception as e:
            logger.error(f'Error taking down loan_defaults tables: {e}')

    def test_get_by_loan_id(self):
        actual_output = self.loan_default_entity.get_by_loan_id(135)
        first_record = actual_output[0]
        self.assertEqual(4, first_record.id)
        self.assertEqual(91, first_record.bo_id)
        self.assertEqual(Decimal(10267.62), first_record.amount_due)
        self.assertEqual(Decimal(9329.43), first_record.outstanding_principal)
        self.assertEqual(Decimal(28.13), first_record.outstanding_interest)
        # self.assertEqual(910.06, first_record.outstanding_late_fee)
        # self.assertEqual(800.00, first_record.amount_recovered)
        # self.assertEqual('2023-03-30 06:42:30', first_record.created_at)
