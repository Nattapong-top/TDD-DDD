import pytest
from domain.models import ParkingTicket
from domain.value_object import MoneyTHB, ParkingHour


def test_parking_ticket_calculate_money():
    rate = MoneyTHB(value=20.0)
    hour_value = ParkingHour(value=3)
    ticket = ParkingTicket(ticket_id=1)

    fee = ticket.calculate_total(hours=hour_value.value, rate=rate)

    assert fee.value == 60.0
    assert ticket.ticket_id == 1


def test_multiply_money_by_hours():
    # เตรียมของ
    rate = MoneyTHB(value=20.0)
    hour_value = ParkingHour(value=3)
    # คำนวณ
    total_fee = rate.value * hour_value.value
    # ตรวจสอบ
    assert total_fee == 60.0


def test_money_should_not_be_negative():
    # โจทย์: ป๋าต้องการว่า "เงินต้องไม่ติดลบ"
    # ถ้าส่ง -100 เข้าไป ยามต้องเป่านกหวีดด่า (ValueError)
    with pytest.raises(ValueError):
        MoneyTHB(value=-100.0)


def test_money_valid_value():
    # โจทย์: ถ้าส่งเงิน 50 บาทเข้าไป ต้องเก็บค่า 50 ไว้ได้ถูกต้อง
    money = MoneyTHB(value=50.0)
    assert money.value == 50.0