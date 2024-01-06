from decimal import Decimal
from typing import Optional

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from capsphere.common import utils
from capsphere.data.model.data_record import DataRecord


class LoanDefault(DataRecord, BaseModel):
    bo_id: int = 0
    loan_id: int = 0
    amount_due: Decimal = Decimal(0.00)
    outstanding_principal: Decimal = Decimal(0.00)
    outstanding_interest: Decimal = Decimal(0.00)
    outstanding_late_fee: Decimal = Decimal(0.00)
    amount_recovered: Decimal = Decimal(0.00)
    legal_fee: Decimal = Decimal(0.00)
    status: str = ''
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        return LoanDefault(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return utils.to_json(self.to_dict())
