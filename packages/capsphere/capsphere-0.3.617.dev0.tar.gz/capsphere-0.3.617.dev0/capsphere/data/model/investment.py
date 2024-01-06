from typing import Optional
from decimal import Decimal

from pydantic import BaseModel

from capsphere.common import utils
from capsphere.data.model.data_record import DataRecord


class Investment(DataRecord, BaseModel):
    invested_amount: Decimal = Decimal(0.00)
    created_by: str = ''
    updated_by: str = ''
    investor_application_id: int = 0
    loan_id: int = 0
    invested_amount_percent: Decimal = Decimal(0.00)
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        return Investment(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return utils.to_json(self.to_dict())
