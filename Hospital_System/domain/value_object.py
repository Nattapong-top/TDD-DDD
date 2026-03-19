from datetime import datetime, date, timedelta
from enum import Enum
from typing import Tuple, Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator


class DomainValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)


class Name(DomainValueObject):
    value: str = Field(..., min_length=1, max_length=50, pattern=r'^[^\d]+$')

    @field_validator('value')
    @classmethod
    def _must_not_be_blank(cls, v: str) -> str:
        if v.strip() == '':
            raise ValueError('ชื่อห้ามว่างครับ')
        return v


class PhoneNumber(DomainValueObject):
    value: str = Field(..., max_length=10, min_length=10)

    @field_validator('value', mode='before')
    @classmethod
    def _normalize_phone(cls, v: str) -> str:
        return v.replace('-', '')

    @field_validator('value', mode='after')
    @classmethod
    def _start_not_zero(cls, v: str) -> str:
        if not v.startswith('0'):
            raise ValueError('เบอร์โทรขึ้นต้นด้วย 0 เท่านั้นครับ')
        return v

    @field_validator('value')
    @classmethod
    def _must_be_digits(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError('ห้ามมีตัวอักษรครับ')
        return v


class DateOfBirth(DomainValueObject):
    year: int
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)

    @model_validator(mode='after')
    def _must_not_be_future_date_and_over_150_years(self) -> 'DateOfBirth':
        dob = date(self.year, self.month, self.day)
        if dob > date.today():
            raise ValueError('วันเกิดห้ามเป็นวันในอนาคต')

        age_in_years = date.today().year - dob.year
        if age_in_years > 150:
            raise ValueError('อายุห้ามเกิดน 150 ปี')
        return self


class Province(Enum):
    BANGKOK = "กรุงเทพมหานคร"
    CHIANG_MAI = "เชียงใหม่"
    PHUKET = "ภูเก็ต"
    KHON_KAEN = "ขอนแก่น"
    CHONBURI = "ชลบุรี"
    MUKDAHAN = 'มุกดาหาร'


class Address(DomainValueObject):
    house_number: str = Field(..., min_length=1, max_length=50, )
    street: Optional[str] = None
    sub_district: str = Field(..., min_length=1, max_length=50, )
    district: str = Field(..., min_length=1, max_length=50, )
    province: Province
    postal_code: str = Field(..., min_length=5, max_length=5, pattern=r'^\d{5}$')


class PatientRights(Enum):
    GOLD_CARD = 'บัตรทอง'
    SOCIAL_SECURITY = 'ประกันสังคม'
    COMPANY_INSURANCE = 'ประกันบริษัท'

class Rights(DomainValueObject):
    rights_type: PatientRights


class BloodPressure(DomainValueObject):
    systolic: int = Field(..., ge=90, le=140)
    diastolic: int = Field(..., ge=60, le=90)
