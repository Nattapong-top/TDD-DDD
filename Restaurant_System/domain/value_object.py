from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class DomainValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)

class MenuItem(DomainValueObject):
    name: str = Field(..., min_length=1, max_length=20)

class MoneyTHB(DomainValueObject):
    amount: float = Field(..., ge=0, le=1000)

class TableID(DomainValueObject):
    table_id : str = Field(..., min_length=1, max_length=20)

class TableName(DomainValueObject):
    table_name : str = Field(..., min_length=1, max_length=20)

class TableStatus(Enum):
    AVAILABLE = 'available'
    OCCUPIED = 'occupied'

class CustomerID(DomainValueObject):
    customer_id : str = Field(..., min_length=1, max_length=20)

