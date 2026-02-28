import pytest
from pydantic import ValidationError
from parking_system.domain.parking_logic import (
    ParkingSystem, Car, ParkingFullError,  )

def test_should_return_parking_spot_when_park_successfully():
    parking = ParkingSystem()
    result = parking.park(car_id=Car(plate_id='ABC-123'))
    assert result == 'Car ABC-123 parked at Spot 1'

def test_should_raise_error_when_parking_is_full():
    parking = ParkingSystem()
    with pytest.raises(ParkingFullError):
        parking.park(Car(plate_id='FULL-999'))

def test_should_raise_error_when_plate_id_is_empty():
    with pytest.raises(ValidationError):
        Car(plate_id='')