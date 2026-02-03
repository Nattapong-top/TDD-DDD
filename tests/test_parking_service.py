from domain.value_object import ParkingHour, MoneyTHB
from domain.services import ParkingService


def test_caluclate_parking_fee_free_under_15_mins():
    hour = ParkingHour(value=0.2)
    rate = MoneyTHB(value=20.0)
    service = ParkingService()

    total_fee = service.calculate_fee(hour=hour, rate=rate)

    assert total_fee.value == 0.0
    

def test_calculate_parking_fee_3_hour_rate_20():
    hour = ParkingHour(value=2.1)
    rate = MoneyTHB(value=20)
    service = ParkingService()

    total_fee = service.calculate_fee(hour, rate)

    assert total_fee.value == 60.0
    assert isinstance(total_fee, MoneyTHB)