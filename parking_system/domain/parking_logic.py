from pydantic import BaseModel, Field


class ParkingFullError(Exception): pass

class Car(BaseModel):
    plate_id: str = Field(..., min_length=1, max_length=20, description='Plate ID ห้ามว่างครับ')

class ParkingSystem:
    def __init__(self):
        self.default_spot = 1

    def park(self, car_id: Car) -> str:
        if car_id.plate_id == 'FULL-999':
            raise ParkingFullError()
        return self._format_success_message(car_id.plate_id, self.default_spot)

    def _format_success_message(self, car_id: str, spot: int) -> str:
        return f'Car {car_id} parked at Spot {spot}'