from Coffee_Shop.domain.value_object import MoneyTHB, DrinkName


class Shop:
    def __init__(self):
        self.PRICE = {
            'Tea': MoneyTHB(value=20.0),
            'Coffee': MoneyTHB(value=30.0),
        }

    def buy(self, drink_name: DrinkName, payment: MoneyTHB) -> tuple[DrinkName, MoneyTHB]:

        self._validate_drink(drink_name)
        drink_price = self.PRICE.get(drink_name.value)
        change_amount = payment.value - drink_price.value

        return drink_name, MoneyTHB(value=change_amount)

    def _validate_drink(self, drink_name: DrinkName):
        if drink_name.value not in self.PRICE:
            raise DrinkNotInMenu()


class DrinkNotInMenu(Exception):
    pass
