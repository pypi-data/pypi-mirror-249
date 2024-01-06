from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

from capsphere.common import utils
from capsphere.data.model.data_record import DataRecord


# @dataclass
class LoanPayment(DataRecord, BaseModel):
    loan_payment_ref_no: str = ''
    loan_paid_uid: str = ''
    loan_id: int = 0
    created_by: str = ''
    updated_by: str = ''
    loan_payment_type: str = ''
    created_by_id: int = 0
    updated_by_id: int = 0
    is_prepayment: bool = False
    loan_amount_paid: Decimal = Decimal(0.00)
    loan_payment_processing_fee: Decimal = Decimal(0.00)
    fpx_mode: Optional[str] = None
    id: Optional[int] = None
    manual_payment_proof_file: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    loan_amount_verified: Optional[Decimal] = None
    loan_payment_status: Optional[str] = None
    approved_at: Optional[str] = None
    prepayment_fee: Optional[Decimal] = None

    @staticmethod
    def from_dict(data: dict):
        return LoanPayment(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return utils.to_json(self.to_dict())
