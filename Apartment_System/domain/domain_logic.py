# Domain Logic for Apartment_System
from pydantic import BaseModel, Field

class DomainValueObject(BaseModel):
    class Config:
        frozen = True

class PositiveValue(DomainValueObject):  # ← extract ตรงนี้
    value: float = Field(..., gt=0)

class ElectricityUnit(PositiveValue): pass
class ElectricityRate(PositiveValue): pass
class WaterUnit(PositiveValue): pass
class WaterRate(PositiveValue): pass

class MoneyTHB(DomainValueObject):
    amount: float = Field(..., gt=0)

def calculate_electricity_bill(unit: ElectricityUnit, rate: ElectricityRate) -> MoneyTHB:
    total = amount=unit.value * rate.value
    return MoneyTHB(amount=total)