# Domain Logic for Apartment_System
from pydantic import BaseModel, Field, ConfigDict, model_validator
from enum import Enum
from typing import Optional


class DomainValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)

class PositiveValue(DomainValueObject):  # ← extract ตรงนี้
    value: float = Field(..., gt=0)

class MoneyTHB(DomainValueObject):
    amount: float = Field(..., gt=0)

class ElectricityUnit(PositiveValue): pass
class ElectricityRate(PositiveValue): pass
class WaterUnit(PositiveValue): pass
class WaterRate(PositiveValue): pass

class TenantNameEmptyError(Exception): pass
class TenantNameTooLongError(Exception): pass
class RoomAlreadyOccupiedError(Exception): pass
class RoomNotOccupiedError(Exception): pass
class RoomConfigNotSetError(Exception): pass

class DomainConfig(DomainValueObject):
    room_rent: MoneyTHB
    electricity_rate: ElectricityRate
    water_rate: WaterRate


class RoomStatus(Enum):
    VACANT = 'vacant'
    OCCUPIED = 'occupied'

class Tenant(DomainValueObject):
    name: str

    @model_validator(mode='before')
    @classmethod
    def validate_name(cls, value):
        name = value.get('name', '')
        if len(name) > 20:
            raise TenantNameTooLongError('ชื่อยาวเกินไป')
        if len(name) == 0:
            raise TenantNameEmptyError('ชื่อต้องไม่ว่าง')
        return value

def calculate_electricity_bill(unit: ElectricityUnit, rate: ElectricityRate) -> MoneyTHB:
    return calculate_bill(unit, rate)

def calculate_water_bill(unit: WaterUnit, rate: WaterRate) -> MoneyTHB:
    return calculate_bill(unit, rate)


def calculate_bill(unit: PositiveValue, rate: PositiveValue) -> MoneyTHB:
    total = unit.value * rate.value
    return MoneyTHB(amount=total)


def calculate_total_bill(electricity_bill: MoneyTHB, water_bill: MoneyTHB, room_rent: MoneyTHB) -> MoneyTHB:
    total = electricity_bill.amount + water_bill.amount + room_rent.amount
    return MoneyTHB(amount=total)

class Room(DomainValueObject):
    room_number: str = Field(..., min_length=1, max_length=20)
    status: RoomStatus
    tenant: Optional[Tenant] = None
    room_rent: Optional[MoneyTHB] = None
    config: Optional[DomainConfig] = None

    def calculate_monthly_bill(
            self,
            electricity_unit: ElectricityUnit,
            water_unit: WaterUnit,

    ) -> MoneyTHB:
        if self.config is None:
            raise RoomConfigNotSetError('ยังไม่ได้กำหนดราคา Domain Logic')
        electricity_bill = calculate_electricity_bill(electricity_unit, self.config.electricity_rate)
        water_bill = calculate_water_bill(water_unit, self.config.water_rate)
        total = calculate_total_bill(electricity_bill, water_bill, self.room_rent)
        return total

    def assign_tenant(self, tenant: Tenant) -> 'Room':
        if self.status == RoomStatus.OCCUPIED:
            raise RoomAlreadyOccupiedError('ห้องนี้มีผู้เช่าแล้ว')
        new_room = self.model_copy(update={
            'tenant': tenant,
            'status': RoomStatus.OCCUPIED,
        })
        return new_room

    def remove_tenant(self) -> 'Room':
        if self.status == RoomStatus.VACANT:
            raise RoomNotOccupiedError('ห้องนี้ว่างแล้ว')
        new_room = self.model_copy(update={
            'tenant': None,
            'status': RoomStatus.VACANT,
        })
        return new_room