from Coffee_Shop.domain.value_object import MoneyTHB, DrinkName


class Shop:
    PRICE = {
        'Tea': MoneyTHB(value=20.0),
        'Coffee': MoneyTHB(value=30.0),
        'Ovaltine': MoneyTHB(value=15.0),
    }

    def __init__(self, randomly_select):
        self._randomly_select = randomly_select

    def buy(self, drink_name: DrinkName, payment: MoneyTHB) -> tuple[DrinkName, MoneyTHB]:
        final_drink = self._get_final_drink_name(drink_name)
        self._validate_drink(final_drink)
        change_amount = self._bill(final_drink, payment)
        return final_drink, MoneyTHB(value=change_amount)

    def _get_final_drink_name(self, drink_name: DrinkName) -> DrinkName:
        actual_drink_str = drink_name.value
        if actual_drink_str == 'Surprise':
            menu_choice = ['Tea', 'Coffee']
            actual_drink_str = self._randomly_select(menu_choice)
        final_drink = DrinkName(value=actual_drink_str)
        return final_drink

    def _bill(self, drink_name: DrinkName, payment: MoneyTHB) -> float:
        drink_price = self.PRICE.get(drink_name.value)
        if payment.value < drink_price.value:
            raise MoneyNotEnough()
        change_amount = payment.value - drink_price.value
        return change_amount

    def _validate_drink(self, drink_name: DrinkName):
        if drink_name.value not in self.PRICE:
            raise DrinkNotInMenu()


class DrinkNotInMenu(Exception): pass


class MoneyNotEnough(Exception): pass


class MockRandomlySelect:
    def __init__(self):
        self.is_called_with_choices: list[str] = []
    def __call__(self, choices: list[str]) -> str:
        self.is_called_with_choices = choices
        return 'Tea'
