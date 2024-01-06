from datetime import datetime
from typing import Optional

from capsphere.common.date import modify_datestr
from capsphere.data.api.payex.payex import verify_response, PayexAuthCode
from capsphere.data.db.entity import LoanPaymentEntity
from capsphere.data.db.entity.abstract_entity import DbEntity
from capsphere.data.db.entity.ledger_entry_entity import LedgerEntryEntity
from capsphere.data.db.entity.loan_amortization_entity import LoanAmortizationEntity
from capsphere.data.db.entity.loan_default_entity import LoanDefaultEntity
from capsphere.data.db.entity.loan_entity import LoanEntity
from capsphere.data.db.entity.loan_statement_entity import LoanStatementEntity
from capsphere.data.model.enum.payment_status import LoanPaymentStatus
from capsphere.data.model.loan import Loan
from capsphere.data.model.loan_payment import LoanPayment
from capsphere.data.utils import get_loan_stage, calculate_interest_rate
from capsphere.service import DataProcessor


class PaymentCallbackHandler(DataProcessor[DbEntity, list[DbEntity]]):
    """
    This class processes the callback from a loan payment either manually or via FPX
    """

    def __init__(self,
                 data: dict,
                 loan_payment_entity: LoanPaymentEntity,
                 loan_statement_entity: LoanStatementEntity,
                 loan_amortization_entity: LoanAmortizationEntity,
                 loan_default_entity: LoanDefaultEntity,
                 ledger_entry_entity: LedgerEntryEntity,
                 loan_record_entity: LoanEntity):
        super().__init__(data,
                         loan_payment_entity=loan_payment_entity,
                         loan_statement_entity=loan_statement_entity,
                         loan_amortization_entity=loan_amortization_entity,
                         loan_default_entity=loan_default_entity,
                         ledger_entry_entity=ledger_entry_entity,
                         loan_record_entity=loan_record_entity)
        self.loan_payment_entity = loan_payment_entity
        self.loan_statement_entity = loan_statement_entity
        self.loan_amortization_entity = loan_amortization_entity
        self.loan_default_entity = loan_default_entity
        self.ledger_entry_entity = ledger_entry_entity
        self.loan_record_entity = loan_record_entity

    def process(self) -> list[DbEntity]:
        ref_no = self.data.get("reference_number")

        """Make sure to handle status of loan_payment id creation here via a queue (probably SQS). Depends if 
        loan_payment_ref_no is either PROCESSING, COMPLETE, or FAILED"""

        """
        IF PROCESSING
        Retry 3 times and then log if still processing
        """
        """
        IF FAILED
        log failure
        """
        """
        IF COMPLETE...
        """
        loan_payment = self.loan_payment_entity.get_by_loan_payment_ref_no(ref_no)[0]
        loan_id = loan_payment.loan_id

        latest_loan_amortization = self.loan_amortization_entity.get_latest(loan_id)
        total_loan_amortizations = self.loan_amortization_entity.get_by_loan_id(loan_id)

        loan_record = self.loan_record_entity.get_by_id(loan_id)[0]
        loan_default_record = self.loan_default_entity.get_by_loan_id(loan_id)[0]
        latest_loan_statement = self.loan_statement_entity.get_by_loan_id(loan_id)[0]

        current_date = datetime.today().strftime("%Y-%m-%d")
        expired_date = modify_datestr(latest_loan_amortization.due_date, months=1)

        loan_default_date = loan_default_record if loan_record is not None else None
        loan_stage = get_loan_stage(loan_record, current_date, expired_date)

        loan_rate = calculate_interest_rate(loan_record.is_shariah, loan_record.loan_interest_rate, loan_stage)

        return []


class ManualCallbackHandler:
    pass


class FpxCallbackHandler(DataProcessor[DbEntity, list[DbEntity]]):
    def __init__(self,
                 data: dict,
                 loan_payment_entity: LoanPaymentEntity):
        super().__init__(data,
                         loan_payment_entity=loan_payment_entity)

        self.loan_payment_ref_no = data.get("loan_payment_ref_no")
        self.fpx_mode = data.get("fpx_mode")
        self.txn_id = data.get("txn_id")
        self.auth_code = data.get("auth_code")

        self.loan = loan_payment_entity.get_loan_by_loan_payment_ref_no(self.loan_payment_ref_no)[0]
        self.business_owner = loan_payment_entity.get_owner_by_loan_payment_ref_no(self.loan_payment_ref_no)[0]
        self.loan_payment = loan_payment_entity.get_loan_by_loan_payment_ref_no(self.loan_payment_ref_no)[0]

    def process(self) -> list[DbEntity]:
        # TODO
        """
        IF no loan_payment with ref number, raise exception here immediately
        """

        match self.auth_code:
            case PayexAuthCode.SUCCESS:
                match self.loan_payment.loan_status:
                    case LoanPaymentStatus.MANAGER_APPROVED:
                        ## update loan amortization borrower paid
                        pass
                    case _:
                        ## approve loan payment full and partial
                        pass
            case PayexAuthCode.PENDING | PayexAuthCode.PENDING_2:
                match self.fpx_mode:
                    case PayexAuthCode.CORPORATE_MODE:
                        ## if corporate and is pending for checker, do nothing as a command will ping server for status
                        pass
                    case _:
                        pass
            case _:
                ## reject loan payment
                pass

        # if verify_response(self.data):
        #     pass
        # else:
        #     pass
