from parking_system.domain.parking_logic import ParkingSystem, Car

def test_should_return_parking_spot_when_park_successfully():
    parking = ParkingSystem()
    result = parking.park(car_id=Car(plate_id='ABC-123'))
    assert result == 'Car ABC-123 parked at Spot 1'

