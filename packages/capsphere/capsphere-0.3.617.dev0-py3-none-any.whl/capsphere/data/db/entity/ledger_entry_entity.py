from capsphere.data.db.entity.abstract_entity import DbEntity
from capsphere.data.db.helpers.utils import get_model_list_from_query
from capsphere.data.model.ledger_entry import LedgerEntry


class LedgerEntryEntity(DbEntity):

    def get_by_user_id(self, user_id: int) -> list[LedgerEntry]:
        query_string = "SELECT * FROM ledger_entries WHERE user_id = %s"
        query_result = self.db_query_service.execute(query_string, (user_id,))
        data = get_model_list_from_query(query_result, LedgerEntry)

        return data

    def get_latest_entry_by_user_id(self, user_id: int) -> LedgerEntry:
        query_string = "SELECT * FROM ledger_entries WHERE user_id = %s ORDER BY id DESC"
        query_result = self.db_query_service.execute(query_string, (user_id,))
        data = get_model_list_from_query(query_result, LedgerEntry)

        if data:
            return data[0]
        else:
            raise ValueError(f"Empty list returned from ledger_entries table for user_id: {user_id}")

    def create(self, issuer_default: LedgerEntry):
        # TODO logic.py line 254
        insert_query = ("INSERT INTO ledger_entries (user_id,reason,credit,debit,amount,balance,"
                        "ledgerable_id,ledgerable_type,ref_code,due_date,loan_payment_id) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,)")

        return self.db_query_service.execute(insert_query, tuple([
            issuer_default.user_id, issuer_default.reason, issuer_default.credit, issuer_default.debit,
            issuer_default.amount, issuer_default.balance, issuer_default.ledgerable_id,
            issuer_default.ledgerable_type, issuer_default.ref_code, issuer_default.due_date,
            issuer_default.loan_payment_id
        ]))
