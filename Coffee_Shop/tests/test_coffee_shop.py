from pytest import raises

from Coffee_Shop.domain.shop_logic import (
    Shop, DrinkNotInMenu, MoneyNotEnough, MockRandomlySelect)
from Coffee_Shop.domain.value_object import DrinkName, MoneyTHB


def test_should_return_tea_change_30_when_buying_tea_with_50_baht():
    mock_selector = MockRandomlySelect()
    shop = Shop(randomly_select=mock_selector)

    order = DrinkName(value='Tea')
    pay = MoneyTHB(value=50.0)

    drink, change = shop.buy(order, pay)

    assert drink.value == 'Tea'
    assert change.value == 30.0


def test_should_return_coffee_change_70_baht_when_buying_coffee_with_100_baht():
    mock_selector = MockRandomlySelect()
    shop = Shop(randomly_select=mock_selector)
    order = DrinkName(value='Coffee')
    pay = MoneyTHB(value=100.0)

    drink, change = shop.buy(order, pay)

    assert drink.value == 'Coffee'
    assert change.value == 70.0


def test_should_raise_DrinkNotInMenu_when_buying_cocoa():
    mock_selector = MockRandomlySelect()
    shop = Shop(randomly_select=mock_selector)
    order = DrinkName(value='Cocoa')
    pay = MoneyTHB(value=50.0)

    with raises(DrinkNotInMenu):
        shop.buy(order, pay)


def test_should_raise_MoneyNotEnough_when_buying_coffee_with_1_baht():
    mock_selector = MockRandomlySelect()
    shop = Shop(randomly_select=mock_selector)
    order = DrinkName(value='Coffee')
    pay = MoneyTHB(value=1.0)
    with raises(MoneyNotEnough):
        shop.buy(order, pay)


def test_should_randomly_select_a_drink_between_tea_and_coffee_when_buying_surprise():
    mock_selector = MockRandomlySelect()
    shop = Shop(randomly_select=mock_selector)
    order = DrinkName(value='Surprise')
    pay = MoneyTHB(value=100.0)
    shop.buy(order, pay)
    assert mock_selector.is_called_with_choices == ['Tea', 'Coffee']


def test_should_return_ovaltine_change_15_baht_when_buying_ovaltine_with_15_baht():
    mock_selector = MockRandomlySelect()
    shop = Shop(randomly_select=mock_selector)
    order = DrinkName(value='Ovaltine')
    pay = MoneyTHB(value=5.0)

    with raises(MoneyNotEnough):
        shop.buy(order, pay)