from pydantic import BaseModel, Field

class MenuItem(BaseModel):
    value: str = Field(..., min_length=1, max_length=20)

class MoneyTHB(BaseModel):
    value: float = Field(..., ge=0, le=1000)

