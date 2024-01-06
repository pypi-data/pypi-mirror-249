from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel

from capsphere.common import utils
from capsphere.data.model.data_record import DataRecord


class BusinessOwnerApplication(DataRecord, BaseModel):
    bo_no: str = ''
    bo_first_name: str = ''
    bo_last_name: str = ''
    user_id: int = 0
    bo_business_name: str = ''
    bo_identification_card_number: str = ''
    bo_date_of_birth: str = ''
    bo_gender: str = ''
    bo_personal_street: str = ''
    bo_personal_city: str = ''
    bo_personal_state: str = ''
    bo_personal_zipcode: str = ''
    bo_personal_country: str = ''
    bo_personal_phonenumber: int = 0
    bo_business_street: str = ''
    bo_business_city: str = ''
    bo_business_state: str = ''
    bo_business_zipcode: str = ''
    bo_business_country: str = ''
    bo_business_phonenumber: int = 0
    bo_industry: str = ''
    bo_legal_entity: str = ''
    bo_no_of_employees: int = 0
    bo_no_of_customers_per_year: int = 0
    bo_registration_number: str = ''
    bo_registration_year: int = 0
    bo_court_judgement: str = ''
    bo_bank_name: str = ''
    bo_bank_account: int = 0
    bo_agree_terms: bool = False
    bo_agree_fees: bool = False
    bo_app_status: str = ''
    bo_status: str = ''
    id: Optional[int] = None
    bo_remark: Optional[str] = None
    bo_registered_country: Optional[str] = None
    bo_registered_street: Optional[str] = None
    bo_registered_city: Optional[str] = None
    bo_registered_state: Optional[str] = None
    bo_registered_zipcode: Optional[str] = None
    bo_business_phone_country_code: Optional[int] = None
    bo_company_activities: Optional[str] = None
    existing_approved_limit_amount: Optional[float] = None
    existing_approved_limit_date: Optional[str] = None
    new_approved_limit_amount: Optional[float] = None
    new_approved_limit_date: Optional[str] = None
    bo_court_judgement_yes: Optional[str] = None
    bo_personal_phone_country_code: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        return BusinessOwnerApplication(**data)

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return utils.to_json(self.to_dict())
