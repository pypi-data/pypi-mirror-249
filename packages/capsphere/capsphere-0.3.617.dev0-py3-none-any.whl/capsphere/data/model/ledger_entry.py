from typing import Optional

from pydantic import BaseModel
from decimal import Decimal

from capsphere.common import utils
from capsphere.data.model.data_record import DataRecord


class LedgerEntry(DataRecord, BaseModel):
    user_id: int = 0
    ledgerable_id: int = 0
    ledgerable_type: str = ''
    ref_code: str = ''
    reason: str = ''
    credit: int = 0
    debit: int = 0
    amount: Decimal = Decimal(0.00)
    balance: Decimal = Decimal(0.00)
    id: Optional[int] = None
    loan_payment_id: Optional[int] = None
    due_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        return LedgerEntry(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return utils.to_json(self.to_dict())
