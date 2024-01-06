from capsphere.data.db.entity.abstract_entity import DbEntity
from capsphere.data.db.helpers.utils import get_model_list_from_query
from capsphere.data.model.loan_default import LoanDefault


class LoanDefaultEntity(DbEntity):
    def get_by_loan_id(self, loan_id: int) -> list[LoanDefault]:
        query_string = "SELECT * FROM loan_defaults WHERE loan_id = %s"
        query_result = self.db_query_service.execute(query_string, (loan_id,))
        data = get_model_list_from_query(query_result, LoanDefault)

        return data
