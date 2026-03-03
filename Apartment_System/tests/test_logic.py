# Unit Tests for Apartment_System
from pytest import raises
from pydantic import ValidationError

from Apartment_System.domain.domain_logic import (
    ElectricityUnit, ElectricityRate, WaterUnit, WaterRate,
    MoneyTHB, calculate_electricity_bill, calculate_water_bill,
    calculate_total_bill)

from Apartment_System.domain.domain_logic import Room, Tenant

def test_should_create_electricity_unit_with_valid_value() -> None:
    valid_unit = 100.0
    unit = ElectricityUnit(value=valid_unit)
    assert unit.value == valid_unit

def test_should_raise_error_when_unit_is_negative() -> None:
    unit = -10.0
    with raises(ValidationError):
        ElectricityUnit(value=unit)

def test_should_create_electricity_rate_por_unit_with_valid_value() -> None:
     rate_valid = 8.0
     rate = ElectricityRate(value=rate_valid)
     assert rate.value == rate_valid

def test_should_raise_error_when_rate_is_negative() -> None:
    rate = -10.0
    with raises(ValidationError):
        ElectricityRate(value=rate)

def test_should_create_water_unit_with_valid_value() -> None:
    valid_unit = 100.0
    unit = WaterUnit(value=valid_unit)
    assert unit.value == valid_unit

def test_should_raise_error_when_water_unit_is_negative() -> None:
    unit = -10.0
    with raises(ValidationError):
        WaterUnit(value=unit)

def test_should_create_water_rate_with_valid_value() -> None:
    water_rate = 19.0
    rate = WaterRate(value=water_rate)
    assert rate.value == water_rate

def test_should_raise_error_when_water_rate_is_negative() -> None:
    rate = -10.0
    with raises(ValidationError):
        WaterRate(value=rate)

def test_should_create_MoneyTHB_with_valid_amount() -> None:
    amount = 100.0
    money = MoneyTHB(amount=amount)
    assert money.amount == amount

def test_should_calculate_electricity_bill() -> None:
    unit = ElectricityUnit(value=100.0)
    rate = ElectricityRate(value=8.0)
    bill = calculate_electricity_bill(unit=unit, rate=rate)
    assert bill.amount == 800.0

def test_should_calculate_water_bill() -> None:
    unit = WaterUnit(value=10.0)
    rate = WaterRate(value=19.0)
    bill = calculate_water_bill(unit=unit, rate=rate)
    assert bill.amount == 190.0

def test_should_calculate_total_bill() -> None:
    e_bill = MoneyTHB(amount=800.0)
    w_bill = MoneyTHB(amount=190.0)
    room_rent = MoneyTHB(amount=5000.0)

    total = calculate_total_bill(
        electricity_bill=e_bill,
        water_bill=w_bill,
        room_rent=room_rent,
    )
    assert total.amount == 5990.0

def test_should_create_room_with_valid_value() -> None:
    room = Room(room_number='101')
    assert room.room_number == '101'

def test_should_raise_error_when_room_number_is_empty() -> None:
    with raises(ValidationError):
        room = Room(room_number='')

def test_should_tenant_with_valid_name() -> None:
    tenant = Tenant(name='nattapong')
    assert tenant.name == 'nattapong'

def test_should_raise_error_when_tenant_name_is_empty() -> None:
    with raises(ValidationError):
        tenant = Tenant(name='')

def test_should_raise_error_when_tenant_name_is_too_long() -> None:
    with raises(ValidationError):
        Tenant(name='a' * 21)


