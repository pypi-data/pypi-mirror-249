from capsphere.data.db.entity.abstract_entity import DbEntity
from capsphere.data.db.helpers.utils import get_model_list_from_query
from capsphere.data.model.loan_statement import LoanStatement


class LoanStatementEntity(DbEntity):

    # TODO here ORDER BY DESC for some reason
    def get_by_loan_id(self, loan_id: int) -> list[LoanStatement]:
        query_string = "SELECT * FROM loan_statements WHERE loan_id = %s ORDER BY id DESC"
        query_result = self.db_query_service.execute(query_string, (loan_id,))

        data = get_model_list_from_query(query_result, LoanStatement)

        return data

    def create(self, loan_statement: LoanStatement):
        # TODO check
        insert_query = ('''
            INSERT INTO loan_statements (id, loan_id, amort_id, month, interest, principal, amount_paid, 
            os_late_interest, os_late_interest_paid, os_late_interest_short, os_interest, os_interest_paid, 
            os_interest_short, current_interest_paid, current_interest_short, total_interest_short, os_principal, 
            os_principal_paid, os_principal_short, current_principal_paid, current_principal_short, 
            total_principal_short, current_late_interest, overdue_days, current_late_interest_paid, partial_interest, 
            partial_interest_discount, total_late_interest, next_payment_amount, pay_before_due, due_date, 
            created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''')
        query_result = self.db_query_service.execute(insert_query, tuple(
            [loan_statement.id,
             loan_statement.loan_id,
             loan_statement.amort_id,
             loan_statement.month,
             loan_statement.interest,
             loan_statement.principal,
             loan_statement.amount_paid,
             loan_statement.os_late_interest,
             loan_statement.os_late_interest_paid,
             loan_statement.os_late_interest_short,
             loan_statement.os_interest,
             loan_statement.os_interest_paid,
             loan_statement.os_interest_short,
             loan_statement.current_interest_paid,
             loan_statement.current_interest_short,
             loan_statement.total_interest_short,
             loan_statement.os_principal,
             loan_statement.os_principal_paid,
             loan_statement.os_principal_short,
             loan_statement.current_principal_paid,
             loan_statement.current_principal_short,
             loan_statement.total_principal_short,
             loan_statement.current_late_interest,
             loan_statement.overdue_days,
             loan_statement.current_late_interest_paid,
             loan_statement.partial_interest,
             loan_statement.partial_interest_discount,
             loan_statement.total_late_interest,
             loan_statement.next_payment_amount,
             loan_statement.pay_before_due,
             loan_statement.due_date,
             loan_statement.created_at,
             loan_statement.updated_at
             ]))

        return query_result
