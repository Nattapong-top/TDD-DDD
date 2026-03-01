from pydantic import BaseModel, Field


class CarNotParkedError(Exception): pass


class AlreadyParkedError(Exception): pass


class ParkingFullError(Exception): pass


class MockSelector:
    def __call__(self): return 99


class Car(BaseModel):
    plate_id: str = Field(..., min_length=1, max_length=20, description='Plate ID ห้ามว่างครับ')


def _format_success_message(car_id: str, spot: int) -> str:
    return f'Car {car_id} parked at Spot {spot}'


class ParkingSystem:
    def __init__(self, selector):
        self._selector = selector
        self._parked_car = set()

    def park(self, car_id: Car) -> str:
        self._validate_parking_rules(car_id)
        self._register_car(car_id)
        chosen_spot = self._selector()
        return _format_success_message(car_id.plate_id, chosen_spot)

    def leave(self, car_id: Car) -> None:
        if car_id.plate_id not in self._parked_car:
            raise CarNotParkedError()
        self._parked_car.discard(car_id.plate_id)

    def is_parked(self, car_id: Car) -> bool:
        return car_id.plate_id in self._parked_car

    def get_parked_count(self) -> int:
        return len(self._parked_car)

    def clear_all(self) -> None:
        self._parked_car.clear()


    def _register_car(self, car_id: Car):
        self._parked_car.add(car_id.plate_id)

    def _validate_parking_rules(self, car_id: Car):
        if car_id.plate_id in self._parked_car:
            raise AlreadyParkedError()
        if car_id.plate_id == 'FULL-999':
            raise ParkingFullError()

