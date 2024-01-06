import logging
import os
import unittest

from dotenv import load_dotenv

from capsphere.data.db import DbQueryService
from capsphere.data.db.connector.postgres import PostgresConnector
from capsphere.data.db.entity.loan_statement_entity import LoanStatementEntity
from capsphere.data.db.entity.test.db_setup import run_sql_script, drop_table

load_dotenv()

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class TestLoanStatementEntity(unittest.TestCase):
    db_query_service = DbQueryService(PostgresConnector())
    loan_statement_entity = LoanStatementEntity(db_query_service)

    @classmethod
    def setUpClass(cls):
        try:
            logger.info('Creating and inserting data for loan_statements tables...')
            run_sql_script('scripts/loan_statements.sql')
            logger.info('Running tests for loan_statements...')
        except Exception as e:
            logger.error(f'setup error:{e}. Running tearDownClass')
            cls.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        logger.info('Dropping tables...')
        try:
            if cls.db_query_service:
                drop_table('loan_statements')
            logger.info('Dropped loan_statements table')
        except Exception as e:
            logger.error(f'Error taking down loan_statements tables: {e}')

    def test_get_by_loan_id(self):
        actual_output = self.loan_statement_entity.get_by_loan_id(127)
        first_record = actual_output[0]
        self.assertEqual(1581, first_record.id)
