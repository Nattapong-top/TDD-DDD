from pydantic import BaseModel


class Car(BaseModel):
    plate_id: str

class ParkingSystem:
    def __init__(self):
        self.default_spot = 1

    def park(self, car_id: Car) -> str:
        return self._format_success_message(car_id.plate_id, self.default_spot)

    def _format_success_message(self, car_id: str, spot: int) -> str:
        return f'Car {car_id} parked at Spot {spot}'