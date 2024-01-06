from capsphere.data.db.entity.abstract_entity import DbEntity
from capsphere.data.db.helpers.utils import get_model_list_from_query, map_row_to_dataclass
from capsphere.data.model.application import BusinessOwnerApplication
from capsphere.data.model.loan import Loan

from capsphere.data.model.loan_payment import LoanPayment


class LoanPaymentEntity(DbEntity):
    def get_by_loan_payment_ref_no(self, loan_payment_ref_no: str) -> list[LoanPayment]:
        select_query = "SELECT * FROM loan_payments WHERE loan_payment_ref_no = %s"
        query_result = self.db_query_service.execute(select_query, (loan_payment_ref_no,))
        data = get_model_list_from_query(query_result, LoanPayment)

        return data

    def get_loan_by_loan_payment_ref_no(self, loan_payment_ref_no: str) -> list[Loan]:
        select_query = ("SELECT loans.* FROM loans JOIN loan_payments ON loans.id = loan_payments.loan_id "
                        "WHERE loan_payments.loan_payment_ref_no = %s")

        query_result = self.db_query_service.execute(select_query, (loan_payment_ref_no,))
        data = get_model_list_from_query(query_result, Loan)

        return data

    def get_owner_by_loan_payment_ref_no(self, loan_payment_ref_no: str) -> list[BusinessOwnerApplication]:
        select_query = ("SELECT business_owner_applications.* FROM business_owner_applications "
                        "JOIN loans ON business_owner_applications.user_id = loans.user_id "
                        "JOIN loan_payments ON loans.id = loan_payments.loan_id "
                        "WHERE loan_payments.loan_payment_ref_no = %s")

        query_result = self.db_query_service.execute(select_query, (loan_payment_ref_no,))
        data = get_model_list_from_query(query_result, BusinessOwnerApplication)

        return data

    def create(self, payment: LoanPayment) -> LoanPayment:
        # TODO logic.py line 19 CHECK
        insert_query = (
            "INSERT INTO loan_payments (loan_amount_paid, loan_payment_ref_no,"
            "loan_payment_processing_fee, loan_paid_uid,loan_id,created_by,"
            "updated_by,created_by_id,updated_by_id, loan_payment_type, manual_payment_proof_file, fpx_mode) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *"
        )
        result = self.db_query_service.execute(insert_query, tuple(
            [payment.loan_amount_paid, payment.loan_payment_ref_no,
             payment.loan_payment_processing_fee, payment.loan_paid_uid, payment.loan_id, payment.created_by,
             payment.updated_by, payment.created_by_id, payment.updated_by_id, payment.loan_payment_type,
             payment.manual_payment_proof_file, payment.fpx_mode]))
        values, headers = result
        return map_row_to_dataclass(LoanPayment, values[0], headers)

    def update(self, payment: LoanPayment) -> LoanPayment:
        loan_payment_ref_no = payment.loan_payment_ref_no
        if not loan_payment_ref_no:
            raise ValueError("payment_reference_no is required to update loan payment")

        verify_loan_exists = self.get_by_loan_payment_ref_no(loan_payment_ref_no)

        if not verify_loan_exists:
            raise ValueError(
                f"loan_payment_ref_no: {loan_payment_ref_no} does not exist in loan_payments table. Please check that "
                f"the loan payment record has already been created")

        update_query = (
            "UPDATE loan_payments SET fpx_mode = %s, "
            "loan_amount_verified = %s, loan_payment_status = %s, "
            "approved_at = %s WHERE loan_payment_ref_no=%s RETURNING *"
        )
        result = self.db_query_service.execute(update_query, tuple(
            [payment.fpx_mode, payment.loan_amount_verified, payment.loan_payment_status, payment.approved_at,
             loan_payment_ref_no]))
        values, headers = result
        return map_row_to_dataclass(LoanPayment, values[0], headers)
