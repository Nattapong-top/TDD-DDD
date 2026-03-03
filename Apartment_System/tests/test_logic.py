# Unit Tests for Apartment_System
from pytest import raises
from pydantic import ValidationError

from Apartment_System.domain.domain_logic import (
    ElectricityUnit, ElectricityRate, WaterUnit, WaterRate)


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