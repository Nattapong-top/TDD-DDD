from pydantic import BaseModel, Field

class MoneyTHB(BaseModel):
    value: float = Field(..., ge=0.0, description='จำนวนเงินต้องไม่ติดลบ')

class DrinkName(BaseModel):
    value: str = Field(..., min_length=1, description='ชื่อเครื่องดื่มห้ามว่าง')

