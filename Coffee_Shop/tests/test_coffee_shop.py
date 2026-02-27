from pytest import raises


from Coffee_Shop.domain.shop_logic import Shop, DrinkNotInMenu,MoneyNotEnough
from Coffee_Shop.domain.value_object import DrinkName, MoneyTHB

def test_should_return_tea_change_30_when_buying_tea_with_50_baht():
    shop = Shop()

    order = DrinkName(value='Tea')
    pay = MoneyTHB(value=50.0)

    drink, change = shop.buy(order, pay)

    assert drink.value == 'Tea'
    assert change.value == 30.0

def test_should_return_coffee_change_70_baht_when_buying_coffee_with_100_baht():
    shop = Shop()
    order = DrinkName(value='Coffee')
    pay = MoneyTHB(value=100.0)

    drink, change = shop.buy(order, pay)

    assert drink.value == 'Coffee'
    assert change.value == 70.0

def test_should_raise_DrinkNotInMenu_when_buying_cocoa():
    shop = Shop()
    order = DrinkName(value='Cocoa')
    pay = MoneyTHB(value=50.0)

    with raises(DrinkNotInMenu):
        shop.buy(order, pay)

def test_should_raise_MoneyNotEnough_when_buying_coffee_with_1_baht():
    shop = Shop()
    order = DrinkName(value='Coffee')
    pay = MoneyTHB(value=1.0)
    with raises(MoneyNotEnough):
        shop.buy(order, pay)
