from pydantic import BaseModel

from domain.value_object import FirstName, LastName

class Employee(BaseModel):
    # Identity (ไอ-เดน-ทิ-ตี้): ตัวตนที่ไม่มีวันเปลี่ยน
    emp_id: int

    # Attributes (แอท-ทริ-บิวท์): คุณลักษณะที่ใช้ Value Object ที่ป๋าปั้นมา
    first_name: FirstName
    last_name: LastName

    # Domain Logic : กฎธุรกิจที่อยู่ภายใน Entity
    def get_full_name(self) -> str:
        # เราดึง .value ออกมาจากกล่อง FirstName และ LastName มาต่อกัน
        return f'{self.first_name.value} {self.last_name.value}'
    