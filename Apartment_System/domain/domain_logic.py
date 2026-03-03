# Domain Logic for Apartment_System
from pydantic import BaseModel, Field

class DomainValueObject(BaseModel):
    class Config:
        frozen = True

class ElectricityUnit(DomainValueObject):
    value: float = Field(..., gt=0)

class ElectricityRate(DomainValueObject):
    value: float = Field(..., gt=0)

class WaterUnit(DomainValueObject):
    value: float = Field(..., gt=0)

class WaterRate(DomainValueObject):
    value: float = Field(..., gt=0)
