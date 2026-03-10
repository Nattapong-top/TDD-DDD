# Unit Tests for Apartment_System
from prompt_toolkit.history import InMemoryHistory
from pytest import raises
from pydantic import ValidationError

from Apartment_System.domain.domain_logic import (
    ElectricityUnit, ElectricityRate, WaterUnit, WaterRate,
    MoneyTHB, calculate_electricity_bill, calculate_water_bill,
    calculate_total_bill, RoomStatus, DomainConfig,
    TenantNameEmptyError, TenantNameTooLongError,
    RoomAlreadyOccupiedError, RoomNotOccupiedError, RoomConfigNotSetError,
)

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
    room = Room(room_number='101', status=RoomStatus(value='vacant'))
    assert room.room_number == '101'

def test_should_raise_error_when_room_number_is_empty() -> None:
    with raises(ValidationError):
        room = Room(room_number='')

def test_should_tenant_with_valid_name() -> None:
    tenant = Tenant(name='nattapong')
    assert tenant.name == 'nattapong'

def test_should_raise_error_when_tenant_name_is_empty() -> None:
    with raises(TenantNameEmptyError):
        tenant = Tenant(name='')

def test_should_raise_error_when_tenant_name_is_too_long() -> None:
    with raises(TenantNameTooLongError):
        Tenant(name='a' * 21)

def test_should_create_room_with_status_vacant() -> None:
    room = Room(room_number='101', status=RoomStatus(value='vacant'))
    assert room.status.value == 'vacant'

def test_should_raise_error_when_room_status_is_invalid() -> None:
    with raises(ValidationError):
        room = Room(room_number='101', status='hello')

def test_should_assign_tenant_to_room() -> None:
    tenant = Tenant(name='nattapong')
    room = Room(room_number='101', status=RoomStatus.OCCUPIED, tenant=tenant)
    assert room.tenant == tenant

def test_should_create_vacant_room_without_tenant() -> None:
    room = Room(room_number='101', status=RoomStatus.VACANT)
    assert room.tenant == None

def test_should_assign_tenant_to_room() -> None:
    tenant = Tenant(name='nattapong')
    room = Room(room_number='101', tenant=tenant, status=RoomStatus.OCCUPIED)
    assert room.tenant == tenant

def test_should_calculate_room_monthly_bill() -> None:
    config = DomainConfig(
        room_rent=MoneyTHB(amount=5000.0),
        electricity_rate=ElectricityRate(value=8.0),
        water_rate=WaterRate(value=19.0),
    )
    room = Room(room_number='101',
                room_rent=MoneyTHB(amount=5000.0),
                status=RoomStatus.OCCUPIED,
                config = config,
    )
    bill = room.calculate_monthly_bill(
        electricity_unit=ElectricityUnit(value=100.0),
        water_unit=WaterUnit(value=10.0),

    )
    assert bill.amount == 5990.0

def test_should_create_room_with_rent() -> None:
    room = Room(room_number='101', status=RoomStatus.VACANT, room_rent=MoneyTHB(amount=5000.0))
    assert room.room_rent.amount == 5000.0

def test_should_create_domain_config_with_valid_value() -> None:
    config = DomainConfig(
        room_rent=MoneyTHB(amount=5000.0),
        electricity_rate=ElectricityRate(value=8.0),
        water_rate=WaterRate(value=19.0),
    )
    assert config.room_rent.amount == 5000.0
    assert config.electricity_rate.value == 8.0
    assert config.water_rate.value == 19.0

def test_should_assign_tenant_to_room() -> None:
    tenant = Tenant(name='nattapong')
    room = Room(room_number='101', tenant=tenant, status=RoomStatus.VACANT)

    new_room = room.assign_tenant(tenant)

    assert new_room.tenant == tenant
    assert new_room.status == RoomStatus.OCCUPIED


def test_should_remove_tenant_from_room() -> None:
    tenant = Tenant(name='nattapong')
    room = Room(room_number='101', tenant=tenant, status=RoomStatus.OCCUPIED)
    remove_tenant = room.remove_tenant()
    assert remove_tenant.tenant is None
    assert remove_tenant.status == RoomStatus.VACANT

def test_should_raise_error_tenant_empty_name() -> None:
    with raises(TenantNameEmptyError):
        Tenant(name='')

def test_should_raise_error_name_tenant_too_long() -> None:
    with raises(TenantNameTooLongError):
        Tenant(name='a' * 21)

def test_should_raise_error_when_room_is_already_occupied() -> None:
    tenant = Tenant(name='nattapong')
    room = Room(room_number='101', tenant=tenant, status=RoomStatus.OCCUPIED)
    with raises(RoomAlreadyOccupiedError):
        room.assign_tenant(tenant)

def test_should_raise_error_when_room_is_not_occupied() -> None:
    room = Room(room_number='101', status=RoomStatus.VACANT)
    with raises(RoomNotOccupiedError):
        room.remove_tenant()

def test_should_calculate_monthly_bill_with_injected_config() -> None:
    config = DomainConfig(
        room_rent=MoneyTHB(amount=5000.0),
        electricity_rate=ElectricityRate(value=8.0),
        water_rate=WaterRate(value=19.0),
    )
    room = Room(
        room_number='101',
        status=RoomStatus.OCCUPIED,
        room_rent=MoneyTHB(amount=5000.0),
        config=config,
    )
    bill = room.calculate_monthly_bill(
        electricity_unit=ElectricityUnit(value=100.0),
        water_unit=WaterUnit(value=10.0),
    )
    assert bill.amount == 5990.0

def test_should_raise_error_when_config_is_not_set() -> None:
    room = Room(
        room_number='101',
        status=RoomStatus.OCCUPIED,
        room_rent=MoneyTHB(amount=5000.0),
    )
    with raises(RoomConfigNotSetError):
        room.calculate_monthly_bill(
            electricity_unit=ElectricityUnit(value=100.0),
            water_unit=WaterUnit(value=10.0),
        )