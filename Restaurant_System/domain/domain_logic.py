# Domain Logic for Restaurant_System
from pydantic import BaseModel

from Restaurant_System.domain.value_object import MenuItem, MoneyTHB


class Order(BaseModel):
    menu: MenuItem
    price: MoneyTHB

    def calculate_bill(self, menu_item: MenuItem, payment: MoneyTHB) -> tuple[MenuItem, MoneyTHB]:
        change = payment.amount - self.price.amount
        return menu_item, MoneyTHB(amount=change)
