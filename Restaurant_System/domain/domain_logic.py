# Domain Logic for Restaurant_System
from pydantic import BaseModel

from Restaurant_System.domain.custom_error import PaymentNotEnough
from Restaurant_System.domain.value_object import MenuItem, MoneyTHB


class Order(BaseModel):
    menu: MenuItem
    price: MoneyTHB

    def calculate_bill(self, menu_item: MenuItem, payment: MoneyTHB) -> tuple[MenuItem, MoneyTHB]:
        self._validate_amount_payment(payment)
        change = payment.amount - self.price.amount
        return menu_item, MoneyTHB(amount=change)

    def _validate_amount_payment(self, payment: MoneyTHB):
        if payment.amount < self.price.amount:
            raise PaymentNotEnough(f'จ่ายเงินมา {payment.amount} บาท ไม่พอ {self.price.amount - payment.amount} บาท')
