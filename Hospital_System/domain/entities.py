from dataclasses import Field
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, model_validator

from Hospital_System.domain.value_object import (
    Name, PhoneNumber, DateOfBirth, Address, NationalID, Rights)


class DomainEntity(BaseModel):
    model_config = ConfigDict(frozen=False)


class Patient(DomainEntity):
    id: UUID
    nation_id: NationalID
    first_name: Name
    last_name: Name
    phone_number: PhoneNumber
    date_of_birth: DateOfBirth
    registered_address: Address
    current_address: Address
    right: Rights

    def __setattr__(self, name: str, value) -> None:
        # ป้องกันการเปลี่ยนค่า field ที่ห้ามแก้ไข
        # รันทุกครั้งที่มีการ set ค่า field ใดๆ ใน object นี้
        # hasattr เช็คว่า field นั้นมีค่าอยู่แล้วหรือยัง
        # (ถ้ายังไม่มี = กำลังสร้างครั้งแรก → ให้ผ่าน)
        if name in ('id', 'nation_id') and hasattr(self, name):
            raise ValueError(f'ห้ามเปลี่ยน {name} ครับ')

        # ถ้าไม่ใช่ field ต้องห้าม → ให้ Pydantic จัดการต่อตามปกติ
        super().__setattr__(name, value)