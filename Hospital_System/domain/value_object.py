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
