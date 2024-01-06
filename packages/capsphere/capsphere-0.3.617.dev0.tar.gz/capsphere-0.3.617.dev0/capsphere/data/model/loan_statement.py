from decimal import Decimal

from typing import Optional

from pydantic import BaseModel

from capsphere.common import utils
from capsphere.data.model.data_record import DataRecord


class LoanStatement(DataRecord, BaseModel):
    loan_id: int = 0
    amort_id: int = 0
    month: int = 0
    interest: Decimal = Decimal(0.00)
    principal: Decimal = Decimal(0.00)
    amount_paid: Decimal = Decimal(0.00)
    os_late_interest: Decimal = Decimal(0.00)
    os_late_interest_paid: Decimal = Decimal(0.00)
    os_late_interest_short: Decimal = Decimal(0.00)
    os_interest: Decimal = Decimal(0.00)
    os_interest_paid: Decimal = Decimal(0.00)
    os_interest_short: Decimal = Decimal(0.00)
    current_interest_paid: Decimal = Decimal(0.00)
    current_interest_short: Decimal = Decimal(0.00)
    total_interest_short: Decimal = Decimal(0.00)
    os_principal: Decimal = Decimal(0.00)
    os_principal_paid: Decimal = Decimal(0.00)
    os_principal_short: Decimal = Decimal(0.00)
    current_principal_paid: Decimal = Decimal(0.00)
    current_principal_short: Decimal = Decimal(0.00)
    total_principal_short: Decimal = Decimal(0.00)
    current_late_interest: Decimal = Decimal(0.00)
    current_late_interest_paid: Decimal = Decimal(0.00)
    partial_interest: Decimal = Decimal(0.00)
    partial_interest_discount: Decimal = Decimal(0.00)
    total_late_interest: Decimal = Decimal(0.00)
    next_payment_amount: Decimal = Decimal(0.00)
    overdue_days: int = 0
    pay_before_due: bool = False
    id: Optional[int] = None
    due_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        return LoanStatement(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return utils.to_json(self.to_dict())

    def update(self, field_name, new_value):
        if hasattr(self, field_name):
            setattr(self, field_name, new_value)
        else:
            print(f"Field '{field_name}' does not exist in the dataclass")
