from pydantic import BaseModel
from domain.value_object import FirstName, LastName, MoneyTHB


# 1. คลาสแม่ (Base Class) คอยคุมเรื่อง Version
class BaseEntity(BaseModel):
    version: int = 1

    def increment_version(self):
        self.version += 1


# 2. คลาสลูก (Entity) ที่มีความฉลาดในตัว
class ParkingSlot(BaseEntity):
    slot_id: str
    is_vacant: bool = True  # 1. เริ่มต้นให้ว่างไว้ก่อน (True)

    def occupy(self) -> None:
        # 3. เช็คสถานะ "ข้างในตัวมันเอง" (self)
        if not self.is_vacant:
            raise ValueError('ช่องจอดนี้ มีรถเข้าจอดแล้วครับ')
        
        # 4. สั่งเปลี่ยนสถานะในตัวมันเองให้เป็น "ไม่ว่าง"
        self.is_vacant = False

        # สะกิดแม่ให้ช่วยอัปเกรดเวอร์ชัน (ใช้ super)
        super().increment_version()

    def release(self) -> None:
        """พฤติกรรม: ปล่อยรถออก"""
        self.is_vacant = True
        super().increment_version()


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
    

    def change_last_name(self, new_lname:LastName) -> None:
        # นี่คือ Invariant (อิน-แว-เรียนท์ - สิ่งที่ต้องเป็นจริงเสมอ)
        # ตรวจสอบว่านามสกุลใหม่ต้องไม่เหมือนเดิม
        if new_lname.value == self.last_name.value:
            raise ValueError('นามสกุลใหม่ต้องไม่ซ้ำกับของเดิม')
        
        # ถ้าผ่านกฎ ก็ทำการเปลี่ยนค่าข้างใน
        self.last_name = new_lname

    
class ParkingTicket(BaseModel):
    ticket_id: int

    # ฟังก์ชันคำนวณเงิน (Calculate Fee)
    # รับค่า 'ชั่วโมง' เป็นเลขธรรมดา และ 'ราคา' เป็นกล่องเงิน
    # แล้วส่งผลลัพธ์กลับมาเป็น 'กล่องเงิน' (MoneyTHB)
    def calculate_total(self, hours:int, rate:MoneyTHB) -> MoneyTHB:
        amount = hours * rate.value

        # ห่อผลลัพธ์ใส่กล่องเงินก่อนส่งคืน (Encapsulation)
        return MoneyTHB(value=amount)