from pydantic import BaseModel, Field, field_validator, ConfigDict


class DomainValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)

class Name(DomainValueObject):
    value: str = Field(..., min_length=1, max_length=50, pattern=r'^[^\d]+$')

    @field_validator('value')
    @classmethod
    def _must_not_be_blank(cls, v:str) -> str:
        if v.strip() == '':
            raise ValueError('ชื่อห้ามว่างครับ')
        return v

class PhoneNumber(DomainValueObject):
    value: str = Field(..., max_length=10, min_length=10)

    @field_validator('value', mode='before')
    @classmethod
    def _normalize_phone(cls, v:str) -> str:
        return v.replace('-', '')

    @field_validator('value', mode='after')
    @classmethod
    def _start_not_zero(cls, v:str) -> str:
        if not v.startswith('0'):
            raise ValueError('เบอร์โทรขึ้นต้นด้วย 0 เท่านั้นครับ')
        return v

    @field_validator('value')
    @classmethod
    def _must_be_digits(cls, v:str) -> str:
        if not v.isdigit():
            raise ValueError('ห้ามมีตัวอักษรครับ')
        return v

