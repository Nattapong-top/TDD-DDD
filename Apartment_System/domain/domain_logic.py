# Domain Logic for Apartment_System
from pydantic import BaseModel, Field

class ElectricityUnit(BaseModel):
    value: float = Field(..., gt=0)

    class Config:
        frozenset = True