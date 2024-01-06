from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

from capsphere.common import utils
from capsphere.data.model.data_record import DataRecord


class LoanAmortization(DataRecord, BaseModel):
    loan_id: int = 0
    month: int = 0
    created_by: str = ''
    updated_by: str = ''
    monthly_payment: Decimal = Decimal(0.00)
    total_amount_paid: Decimal = Decimal(0.00)
    principal_paid: Decimal = Decimal(0.00)
    amount_remaining: Decimal = Decimal(0.00)
    interest_amount: Decimal = Decimal(0.00)
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    due_date: Optional[str] = None
    paid_status: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        return LoanAmortization(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return utils.to_json(self.to_dict())