# Domain Logic for Apartment_System
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class DomainValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)

class PositiveValue(DomainValueObject):  # ← extract ตรงนี้
    value: float = Field(..., gt=0)

class ElectricityUnit(PositiveValue): pass
class ElectricityRate(PositiveValue): pass
class WaterUnit(PositiveValue): pass
class WaterRate(PositiveValue): pass

class MoneyTHB(DomainValueObject):
    amount: float = Field(..., gt=0)

class RoomStatus(Enum):
    VACANT = 'vacant'
    OCCUPIED = 'occupied'

def calculate_electricity_bill(unit: ElectricityUnit, rate: ElectricityRate) -> MoneyTHB:
    return calculate_bill(unit, rate)

def calculate_water_bill(unit: WaterUnit, rate: WaterRate) -> MoneyTHB:
    return calculate_bill(unit, rate)


def calculate_bill(rate: PositiveValue, unit: PositiveValue) -> MoneyTHB:
    total = unit.value * rate.value
    return MoneyTHB(amount=total)


def calculate_total_bill(electricity_bill: MoneyTHB, water_bill: MoneyTHB, room_rent: MoneyTHB) -> MoneyTHB:
    total = electricity_bill.amount + water_bill.amount + room_rent.amount
    return MoneyTHB(amount=total)

class Room(DomainValueObject):
    room_number: str = Field(..., min_length=1, max_length=20)
    status: RoomStatus

class Tenant(DomainValueObject):
    name: str = Field(..., min_length=1, max_length=20)

