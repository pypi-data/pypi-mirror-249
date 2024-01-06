from datetime import date

from capsphere.data.db.entity.abstract_entity import DbEntity
from capsphere.data.db.helpers.utils import get_model_list_from_query
from capsphere.data.model.loan_amortization import LoanAmortization


class LoanAmortizationEntity(DbEntity):

    def get_by_loan_id(self, loan_id: int) -> list[LoanAmortization]:
        select_query = "SELECT * FROM loan_amortizations WHERE loan_id = %s ORDER BY id"
        query_result = self.db_query_service.execute(select_query, (loan_id,))

        data = get_model_list_from_query(query_result, LoanAmortization)

        return data

    def get_latest(self, loan_id: int) -> LoanAmortization:
        select_query = "SELECT * FROM loan_amortizations WHERE loan_id = %s ORDER BY id DESC"
        query_result = self.db_query_service.execute(select_query, (loan_id,))

        data = get_model_list_from_query(query_result, LoanAmortization)

        if data:
            return data[0]
        else:
            raise ValueError(f"Empty list returned for loan_amortizations table for loan_id: {loan_id}")

    def get_latest_paid_status_not_null(self, loan_id: int) -> LoanAmortization:
        select_query = "SELECT * FROM loan_amortizations WHERE loan_id = %s AND paid_status IS NOT NULL ORDER BY id DESC"
        query_result = self.db_query_service.execute(select_query, (loan_id,))

        data = get_model_list_from_query(query_result, LoanAmortization)

        if data:
            return data[0]
        else:
            raise ValueError(
                f"Empty list returned querying most recent not null for loan_amortizations table for loan_id: {loan_id}")

    def get_by_loan_id_and_month(self, loan_id: int, month: int) -> LoanAmortization:
        select_query = "SELECT * FROM loan_amortizations WHERE loan_id = %s AND Month = %s"
        query_result = self.db_query_service.execute(select_query, (loan_id, month,))

        data = get_model_list_from_query(query_result, LoanAmortization)

        if data:
            if len(data) > 1:
                raise ValueError(
                    f"More than one entry returned from loan_amortizations table for loan_id: {loan_id} and month: {month}")
            else:
                return data[0]
        else:
            raise ValueError(f"Empty list returned from loan_amortizations table for loan_id: {loan_id}")

    def get_latest_missed(self, loan_id: int, record_id: int, due_date: date) -> list[LoanAmortization]:
        select_query = "SELECT * FROM loan_amortizations WHERE loan_id = %s AND id >= %s AND DATE(due_date) <= %s  ORDER BY id ASC"
        query_result = self.db_query_service.execute(select_query, (loan_id, record_id, due_date))

        data = get_model_list_from_query(query_result, LoanAmortization)

        return data

    def update_paid_status(self, paid_status: str, record_id: int):
        # TODO logic.py line 77 DONE
        update_query = "UPDATE loan_amortizations SET paid_status=%s WHERE id=%s"
        update_result = self.db_query_service.execute(update_query, tuple([paid_status, record_id]))
        return update_result
