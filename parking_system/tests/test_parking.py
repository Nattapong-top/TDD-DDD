import pytest
from pydantic import ValidationError
from parking_system.domain.parking_logic import (
    ParkingSystem, Car, ParkingFullError, MockSelector,
    AlreadyParkedError, CarNotParkedError)

def test_should_return_parking_spot_when_park_successfully():
    mock_selector = MockSelector()
    parking = ParkingSystem(selector=mock_selector)
    result = parking.park(car_id=Car(plate_id='ABC-123'))
    assert 'ABC-123' in result
    assert 'Spot 99' in result

def test_should_raise_error_when_parking_is_full():
    mock_selector = MockSelector()
    parking = ParkingSystem(selector=mock_selector)
    with pytest.raises(ParkingFullError):
        parking.park(Car(plate_id='FULL-999'))

def test_should_raise_error_when_plate_id_is_empty():
    with pytest.raises(ValidationError):
        Car(plate_id='')

def test_should_use_selector_to_choose_spot():
    mock_selector = MockSelector()
    parking = ParkingSystem(selector=mock_selector)
    result = parking.park(Car(plate_id='XYZ-789'))
    assert 'Spot 99' in result

def test_should_raise_error_when_parking_duplicate_car():
    mock_selector = MockSelector()
    parking = ParkingSystem(selector=mock_selector)
    car = Car(plate_id='XYZ-789')

    parking.park(car)
    with pytest.raises(AlreadyParkedError):
        parking.park(car)

def test_should_allow_car_to_park_again_after_leaving():
    mock_selector = MockSelector()
    parking = ParkingSystem(selector=mock_selector)
    car = Car(plate_id='EXIT-555')
    parking.park(car)

    parking.leave(car)

    result = parking.park(car)
    assert 'EXIT-555' in result

def test_should_return_true_if_car_is_already_parked():
    mock_selector = MockSelector()
    parking = ParkingSystem(mock_selector)
    car = Car(plate_id='CHECK-123')

    assert parking.is_parked(car) is False
    parking.park(car)
    assert parking.is_parked(car) is True

def test_should_return_correct_count_of_parked_cars():
    parking = ParkingSystem(selector=MockSelector())
    parking.park(Car(plate_id='ABC-123'))
    parking.park(Car(plate_id='XYZ-789'))

    assert parking.get_parked_count() == 2

def test_should_raise_error_when_leaving_with_car_not_in_system():
    parking = ParkingSystem(selector=MockSelector())
    car = Car(plate_id='GHOST-999')

    with pytest.raises(CarNotParkedError):
        parking.leave(car)

def test_should_clear_all_parked_cars():
    parking = ParkingSystem(selector=MockSelector())
    parking.park(Car(plate_id='ABC-123'))
    parking.park(Car(plate_id='XYZ-789'))

    parking.clear_all()

    assert parking.get_parked_count() == 0