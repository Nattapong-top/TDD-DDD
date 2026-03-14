# Domain Logic for Restaurant_System
from typing import Optional

from pydantic import BaseModel, model_validator

from Restaurant_System.domain.custom_error import (
    PaymentNotEnough, OrderNotInMenu, TableAlreadyOccupiedError)
from Restaurant_System.domain.value_object import (MenuItem, MoneyTHB,
    TableID, TableName, DomainValueObject, TableStatus)


class Order(DomainValueObject):
    menu: MenuItem
    available_menus: dict[str, MoneyTHB] = {}

    @property
    def price(self) -> MoneyTHB:
        return self.available_menus[self.menu.name]

    @model_validator(mode='before')
    @classmethod
    def _validate_menus(cls, value):
        menu = value.get('menu')
        available_menus = value.get('available_menus', [])
        if menu.name not in available_menus:
            raise OrderNotInMenu('ไม่มีเมนูนี้ครับ')
        return value

    def calculate_bill(self, menu_item: MenuItem, payment: MoneyTHB) -> tuple[MenuItem, MoneyTHB]:
        self._validate_amount_payment(payment)
        change = payment.amount - self.price.amount
        return menu_item, MoneyTHB(amount=change)

    def _validate_amount_payment(self, payment: MoneyTHB):
        if payment.amount < self.price.amount:
            raise PaymentNotEnough(f'จ่ายเงินมา {payment.amount} บาท ไม่พอ {self.price.amount - payment.amount} บาท')

class Table(DomainValueObject):
    table_id: TableID
    table_name: TableName
    table_status: TableStatus = TableStatus.AVAILABLE
    order: Optional[Order] = None

    def assign_order(self, order: Order) -> 'Table':
        self._validate_status()
        new_table = self.model_copy(update={
            'order': order,
            'table_status': TableStatus.OCCUPIED,
        })
        return new_table

    def clear_order(self) -> 'Table':
        new_table = self.model_copy(update={
            'order': None,
            'table_status': TableStatus.AVAILABLE,
        })
        return new_table

    def _validate_status(self):
        if self.table_status == TableStatus.OCCUPIED:
            raise TableAlreadyOccupiedError('โต๊นี้ยังไม่ว่างครับ')