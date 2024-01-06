from typing import Optional

from decimal import Decimal

from pydantic import BaseModel

from capsphere.common import utils
from capsphere.data.model.data_record import DataRecord


class Loan(DataRecord, BaseModel):
    is_shariah: bool = False
    is_esg: int = 0
    is_guaranteed: bool = False
    is_stopping_late_fee: bool = False
    loan_ref_code: str = ''
    loan_listing_duration: int = 0
    set_mycif_investment_portion: int = 0
    loan_type: str = ''
    loan_duration: int = 0
    require_direct_debit: bool = False
    business_owner_application_id: int = 0
    loan_purpose: str = ''
    created_by: str = ''
    updated_by: str = ''
    bo_approved_for_listing: str = ''
    bo_approved_for_issuance: str = ''
    loan_status: str = ''
    loan_disbursed_status: str = ''
    loan_interest_rate: Decimal = Decimal(0.00)
    loan_amount: Decimal = Decimal(0.00)
    id: Optional[int] = None
    mycif_investment_portion: Optional[Decimal] = None
    stopping_late_fee_date: Optional[str] = None
    financing_type: Optional[str] = None
    user_id: Optional[int] = None
    loan_simple_interest_rate: Optional[Decimal] = None
    manager_investment_notes: Optional[str] = None
    bo_investment_notes: Optional[str] = None
    loan_funded_percent: Optional[Decimal] = None
    loan_funded_amount: Optional[Decimal] = None
    loan_asset_type: Optional[str] = None
    loan_asset_brand: Optional[str] = None
    loan_asset_model_number: Optional[str] = None
    loan_asset_url: Optional[str] = None
    loan_asset_supplier_name: Optional[str] = None
    loan_asset_purchase_price: Optional[int] = None
    loan_asset_purchase_number: Optional[int] = None
    loan_asset_useful_life: Optional[int] = None
    loan_asset_secondary_market: Optional[str] = None
    loan_asset_secondary_market_yes: Optional[str] = None
    loan_asset_salvage: Optional[int] = None
    loan_guarantor_name: Optional[str] = None
    loan_guarantor_nric: Optional[str] = None
    loan_guarantor_mobile: Optional[str] = None
    loan_guarantor_email: Optional[str] = None
    loan_guarantor_address: Optional[str] = None
    loan_guarantor_relationship: Optional[str] = None
    loan_guarantor_checkbox: Optional[int] = None
    loan_service_fee: Optional[Decimal] = None
    loan_stamping_fee: Optional[Decimal] = None
    loan_charge_fee: Optional[Decimal] = None
    loan_success_fee: Optional[Decimal] = None
    loan_bank_charges: Optional[Decimal] = None
    loan_sst: Optional[Decimal] = None
    loan_remark: Optional[str] = None
    loan_factsheet: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    active: Optional[int] = None
    loan_category: Optional[str] = None
    guaranteed_entity: Optional[str] = None
    note_listed_at: Optional[str] = None
    publish_date_at: Optional[str] = None
    investor_fee: Optional[Decimal] = None
    approved_note_status: Optional[str] = None
    loan_asset_supplier_contact_no: Optional[str] = None
    credit_rating: Optional[str] = None
    funded_noti_at: Optional[str] = None
    full_funded_noti_at: Optional[str] = None
    basic_wait_option: Optional[int] = None
    basic_wait_days: Optional[int] = None
    basic_wait_percent: Optional[int] = None

    @staticmethod
    def from_dict(data: dict):
        return Loan(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return utils.to_json(self.to_dict())