# Unit Tests for Restaurant_System
import pytest

from Restaurant_System.domain.value_object import (
    MenuItem, MoneyTHB)

def test_should_create_MenuItem_is_valid():
    menu_item = MenuItem(value='kaparwkaikidow')
    assert menu_item.value == 'kaparwkaikidow'

def test_should_raise_error_when_Menuitem_is_Empty():
    with pytest.raises(ValueError):
        menu_item = MenuItem(value='')

def test_should_raise_error_when_MenuItem_is_name_too_long():
    with pytest.raises(ValueError):
        menu_item = MenuItem(value='kaparwkaikidow'*20)

def test_should_create_MoneyTHB_is_valid():
    money_thb = MoneyTHB(value=50.0)
    assert money_thb.value == 50.0

def test_should_raise_error_when_MoneyTHB_is_negative():
    with pytest.raises(ValueError):
        money_thb = MoneyTHB(value=-1)

def test_should_raise_error_when_MoneyTHB_is_more_than_1000():
    with pytest.raises(ValueError):
        money_thb = MoneyTHB(value=1001)