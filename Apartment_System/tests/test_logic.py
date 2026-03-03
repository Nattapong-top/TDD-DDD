# Unit Tests for Apartment_System
from pytest import raises
from pydantic import ValidationError

from Apartment_System.domain.domain_logic import (
    ElectricityUnit)


def test_should_create_electricity_unit_with_valid_value() -> None:
    valid_unit = 100.0
    unit = ElectricityUnit(value=valid_unit)
    assert unit.value == valid_unit

def test_should_raise_error_when_unit_is_negative() -> None:
    unit = -10.0
    with raises(ValidationError):
        ElectricityUnit(value=unit)

