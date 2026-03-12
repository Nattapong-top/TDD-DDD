# Domain Logic for Restaurant_System
from pydantic import BaseModel

from Restaurant_System.domain.value_object import MenuItem, MoneyTHB


class Order(BaseModel):
    menu: MenuItem
    price: MoneyTHB
