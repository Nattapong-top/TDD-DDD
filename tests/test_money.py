import pytest
from domain.value_object import MoneyTHB


def test_money_should_not_be_negative():
    # โจทย์: ป๋าต้องการว่า "เงินต้องไม่ติดลบ"
    # ถ้าส่ง -100 เข้าไป ยามต้องเป่านกหวีดด่า (ValueError)
    with pytest.raises(ValueError):
        MoneyTHB(value=-100.0)

def test_money_valid_value():
    # โจทย์: ถ้าส่งเงิน 50 บาทเข้าไป ต้องเก็บค่า 50 ไว้ได้ถูกต้อง
    money = MoneyTHB(value=50.0)
    assert money.value == 50.0