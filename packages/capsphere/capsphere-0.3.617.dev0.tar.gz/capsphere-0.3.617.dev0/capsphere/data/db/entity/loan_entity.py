from capsphere.data.db.entity.abstract_entity import DbEntity
from capsphere.data.db.helpers.utils import get_model_list_from_query
from capsphere.data.model.loan import Loan


class LoanEntity(DbEntity):

    def get_by_id(self, loan_id: int) -> list[Loan]:
        query_string = "SELECT * FROM loans WHERE id = %s"
        query_result = self.db_query_service.execute(query_string, (loan_id,))
        data = get_model_list_from_query(query_result, Loan)

        return data
