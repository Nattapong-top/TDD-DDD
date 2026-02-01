import pytest

from domain.value_object import ParkingHour


def test_parking_hour_should_fail_if_negetive():
    # โจทย์: ถ้าส่ง -1 เข้าไป ต้องระเบิด (ValueError)
    with pytest.raises(ValueError):
        ParkingHour(value=-1)
