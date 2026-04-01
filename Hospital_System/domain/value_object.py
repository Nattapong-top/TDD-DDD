from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import (
    BaseModel, Field, field_validator, ConfigDict, model_validator)


class DomainValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)


class Province(Enum):
    BANGKOK = "กรุงเทพมหานคร"
    CHIANG_MAI = "เชียงใหม่"
    PHUKET = "ภูเก็ต"
    KHON_KAEN = "ขอนแก่น"
    CHONBURI = "ชลบุรี"
    MUKDAHAN = 'มุกดาหาร'


class PaymentType(Enum):
    GOLD_CARD = 'บัตรทอง'
    SOCIAL_SECURITY = 'ประกันสังคม'
    COMPANY_INSURANCE = 'ประกันบริษัท'
    CASH = 'เงินสด'
    QR_PAYMENT = 'คิวอาร์โค๊ด'


class Specialization(Enum):
    INTERNAL_MEDICINE = "อายุรกรรม"
    SURGERY = "ศัลยกรรม"
    PEDIATRICS = "กุมารเวชศาสตร์"
    ORTHOPEDICS = "ออร์โธปิดิกส์"
    OBSTETRICS = "สูติกรรม"
    CARDIOLOGY = "โรคหัวใจ"


class QueueStatus(Enum):
    WAITING = 'รอ'
    IN_PROGRESS = 'กำลังพบหมอ'
    COMPLETED = 'เสร็จแล้ว'
    CANCELLED = 'ยกเลิก'


class NationalID(DomainValueObject):
    id: str = Field(..., min_length=13, max_length=13, pattern=r'^\d{13}$')


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
            raise ValueError('อายุห้ามเกิน 150 ปี')
        return self


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


class Weight(DomainValueObject):
    value: float = Field(..., ge=0.2, le=300)


class Height(DomainValueObject):
    value: float = Field(..., ge=30, le=250)


class Temperature(DomainValueObject):
    value: float = Field(..., ge=35, le=42)


class VitalSigns(DomainValueObject):
    blood_pressure: BloodPressure
    weight: Weight
    height: Height
    temperature: Temperature
    symptom: str = Field(..., min_length=1, max_length=50)

    @field_validator('symptom')
    @classmethod
    def _must_not_be_blank(cls, v: str) -> str:
        if v.strip() == '':
            raise ValueError('กรุณาบอกอาการด้วย')
        return v


class MedicineInfo(DomainValueObject):
    name: str = Field(..., min_length=1, max_length=100)
    strength: str = Field(..., min_length=1, max_length=100)
    frequency: str = Field(..., min_length=1, max_length=100)

    @field_validator('name', 'strength', 'frequency')
    @classmethod
    def _must_not_be_blank(cls, v: str) -> str:
        if v.strip() == '':
            raise ValueError('กรุณากรอกข้อมูลด้วยครับ')
        return v


class Diagnosis(DomainValueObject):
    disease: str = Field(..., min_length=1, max_length=100)
    treatment: str = Field(..., min_length=1, max_length=500)
    medicine_prescribed: list[MedicineInfo] = []

    @field_validator('disease', 'treatment')
    @classmethod
    def _must_not_be_blank(cls, v: str) -> str:
        if v.strip() == '':
            raise ValueError('กรุณากรอกข้อมูลด้วยครับ')
        return v


class Payment(DomainValueObject):
    amount: Decimal = Field(..., ge=Decimal('0.01'), le=Decimal('10000000'))
    payment_type: PaymentType


class LicenseNumber(DomainValueObject):
    id: str = Field(..., min_length=7, max_length=7, pattern=r'^ว\.\d{5}$')


class MedicalSpecialty(DomainValueObject):
    value: Specialization


class Number(DomainValueObject):
    id: int = Field(..., ge=0, le=500)

class Version(DomainValueObject):
    number: int = Field(..., ge=1)

    def increment(self) -> 'Version':
        return Version(number=self.number + 1)
