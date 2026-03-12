from pydantic import BaseModel, Field

class MenuItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)

class MoneyTHB(BaseModel):
    amount: float = Field(..., ge=0, le=1000)

