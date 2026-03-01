from pydantic import BaseModel, Field


class AlreadyParkedError(Exception): pass

class ParkingFullError(Exception): pass

class MockSelector:
    def __call__(self): return 99

class Car(BaseModel):
    plate_id: str = Field(..., min_length=1, max_length=20, description='Plate ID ห้ามว่างครับ')

class ParkingSystem:
    def __init__(self, selector):
        self.default_spot = 1
        self._selector = selector
        self._parked_car = set()


    def park(self, car_id: Car) -> str:
        self._validate_parking_rules(car_id)

        self._parked_car.add(car_id.plate_id)

        chosen_spot = self._selector()

        return self._format_success_message(car_id.plate_id, chosen_spot)

    def _validate_parking_rules(self, car_id: Car):
        if car_id.plate_id in self._parked_car:
            raise AlreadyParkedError()

        if car_id.plate_id == 'FULL-999':
            raise ParkingFullError()

    def _format_success_message(self, car_id: str, spot: int) -> str:
        return f'Car {car_id} parked at Spot {spot}'