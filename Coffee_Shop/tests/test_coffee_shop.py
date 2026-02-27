from Coffee_Shop.domain.shop_logic import Shop
from Coffee_Shop.domain.value_object import DrinkName, MoneyTHB

def test_should_return_tea_change_30_when_buying_tea_with_50_baht():
    shop = Shop()

    order = DrinkName(value='Tea')
    pay = MoneyTHB(value=50.0)

    drink, change = shop.buy(order, pay)

    assert drink.value == 'Tea'
    assert change.value == 30.0

