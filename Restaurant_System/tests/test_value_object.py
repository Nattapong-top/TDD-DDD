# Unit Tests for Restaurant_System
import pytest

from Restaurant_System.domain.value_object import (
    MenuItem, MoneyTHB)

def test_should_create_MenuItem_is_valid():
    menu_item = MenuItem(value='kaparwkaikidow')
    assert menu_item.value == 'kaparwkaikidow'

def test_should_create_MoneyTHB_is_valid():
    money_thb = MoneyTHB(value=50.0)
    assert money_thb.value == 50.0