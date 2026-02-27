from Coffee_Shop.domain.value_object import MoneyTHB, DrinkName


class Shop:
    def __init__(self):
        self.PRICE = {
            'Tea': MoneyTHB(value=20.0),
        }

    def buy(self, drink_name: DrinkName, payment: MoneyTHB) -> tuple[DrinkName, MoneyTHB]:
        drink_price = self.PRICE.get(drink_name.value)
        change_amount = payment.value - drink_price.value

        return drink_name, MoneyTHB(value=change_amount)
