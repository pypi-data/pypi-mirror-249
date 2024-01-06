import asyncio
import os
import unittest
from decimal import Decimal

from dotenv import load_dotenv

from capsphere.data.db import DbQueryService, DbQueryServiceAsync
from capsphere.data.db.connector.postgres import PostgresConnector
from capsphere.data.db.connector.postgres.pg_connection import PostgresConnectorAsync
from capsphere.data.db.helpers.utils import get_model_list_from_query
from capsphere.data.model.loan import Loan
from capsphere.data.model.loan_statement import LoanStatement

load_dotenv()

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# @unittest.skip("just testing connection")
class TestExecutor(unittest.TestCase):
    connector = PostgresConnector()

    def test_postgres_executor(self):
        executor_service = DbQueryService(self.connector)
        data = executor_service.execute("SELECT * FROM loan_payments where loan_payment_ref_no = 'LPAY_910202365233M1234567'")

        print(get_model_list_from_query(data, LoanStatement))

    def test_loan_records(self):
        executor_service = DbQueryService(self.connector)
        data = executor_service.execute("SELECT * FROM loans")

        print(get_model_list_from_query(data, Loan))


    # def test_something(self):
    #     executor_service = DbQueryService(self.connector)
    #     loan_statement = LoanStatement(loan_id=198, amort_id=1635, principal=Decimal(88888.88))
    #     executor_service.execute(
    #         "INSERT INTO loan_statements (loan_id, amort_id, month, interest, principal, amount_paid, "
    #         "os_late_interest, os_late_interest_paid, os_late_interest_short, os_interest, os_interest_paid, "
    #         "os_interest_short, current_interest_paid, current_interest_short, total_interest_short, os_principal, "
    #         "os_principal_paid, os_principal_short, current_principal_paid, current_principal_short, "
    #         "total_principal_short, current_late_interest, overdue_days, current_late_interest_paid, partial_interest, "
    #         "partial_interest_discount, total_late_interest, next_payment_amount, pay_before_due, due_date,"
    #         "created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
    #         "%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    #         params=(loan_statement.loan_id,
    #                 loan_statement.amort_id,
    #                 loan_statement.month,
    #                 loan_statement.interest,
    #                 loan_statement.principal,
    #                 loan_statement.amount_paid,
    #                 loan_statement.os_late_interest,
    #                 loan_statement.os_late_interest_paid,
    #                 loan_statement.os_late_interest_short,
    #                 loan_statement.os_interest,
    #                 loan_statement.os_interest_paid,
    #                 loan_statement.os_interest_short,
    #                 loan_statement.current_interest_paid,
    #                 loan_statement.current_interest_short,
    #                 loan_statement.total_interest_short,
    #                 loan_statement.os_principal,
    #                 loan_statement.os_principal_paid,
    #                 loan_statement.os_principal_short,
    #                 loan_statement.current_principal_paid,
    #                 loan_statement.current_principal_short,
    #                 loan_statement.total_principal_short,
    #                 loan_statement.current_late_interest,
    #                 loan_statement.overdue_days,
    #                 loan_statement.current_late_interest_paid,
    #                 loan_statement.partial_interest,
    #                 loan_statement.partial_interest_discount,
    #                 loan_statement.total_late_interest,
    #                 loan_statement.next_payment_amount,
    #                 loan_statement.pay_before_due,
    #                 loan_statement.due_date,
    #                 loan_statement.created_at,
    #                 loan_statement.updated_at),
    #         fetch_results=False)

    def test_mysql_executor(self):
        pass


class TestConnectionAsync(unittest.IsolatedAsyncioTestCase):
    async def test_postgres_executor_async(self):
        connector_async = PostgresConnectorAsync()
        executor_service = DbQueryServiceAsync(connector_async)
        async with connector_async.get_connection_async():
            data = await executor_service.execute_async("SELECT * FROM test_table")
