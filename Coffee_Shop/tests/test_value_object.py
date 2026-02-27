import pytest
from pydantic import ValidationError

from Coffee_Shop.domain.value_object import MoneyTHB, DrinkName

def test_MoneyTHB_cannot_be_negative():
    with pytest.raises(ValidationError):
        invalid_money = MoneyTHB(amount=-10.0)

def test_MoneyTHB_can_be_created_with_valid_amount():
    valid_money = MoneyTHB(amount=50.0)
    assert valid_money.amount == 50.0

def test_MoneyTHB_cannot_empty_money():
    with pytest.raises(ValidationError):
        empty_money = MoneyTHB(amount='')

def test_DrinkName_cannot_be_empty():
    with pytest.raises(ValidationError):
        empty_name = DrinkName(drink='')
