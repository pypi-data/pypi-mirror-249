from datetime import datetime
from decimal import Decimal

from capsphere.data.model.enum import LoanStage
from capsphere.data.model.loan import Loan


def get_loan_stage(loan_record: Loan, current_date: str, expired_date: str) -> LoanStage:
    current_datetime = datetime.strptime(current_date, "%Y-%m-%d")
    expired_datetime = datetime.strptime(expired_date, "%Y-%m-%d")

    if loan_record.approved_note_status == 'Defaulted':
        status = LoanStage.DEFAULTED.value
    elif (current_datetime - expired_datetime).days > 0:
        status = LoanStage.EXPIRED.value
    else:
        status = LoanStage.NORMAL.value

    return status


def calculate_interest_rate(is_shariah: bool, interest_rate: Decimal, loan_stage: LoanStage) -> Decimal:
    if loan_stage == 'DEFAULTED' and interest_rate + 5 > 18:
        return Decimal(18)
    elif is_shariah == 1 and interest_rate + 5 > 10:
        return Decimal(10)
    else:
        return interest_rate + 5
