from pydantic import BaseModel, field_validator, ConfigDict
import math
from typing import Any, ClassVar


class ParkingHour(BaseModel):
    # แช่แข็ง Object ห้ามใครแก้ค่าหลังสร้างเสร็จ
    model_config = ConfigDict(frozen=True)
    value:int
    
    # ใส่ ClassVar[ประเภท] คลุมไว้ เพื่อบอกว่าเป็น "กฎส่วนกลาง"
    MIN_LIMIT: ClassVar[int] = 0
    MAX_LIMT: ClassVar[int] = 24

    @field_validator('value', mode='before')
    @classmethod
    def round_up_and_check_range(cls, v:Any) -> int:
        '''กำหนดชั่วโมงปัดเศษขึ้นและ ไม่น้อยกว่า 0 ไม่เกิน 24'''
        # 1. ลอจิกการปัดเศษ: ใช้สูตรคณิตศาสตร์
        try:
            rounded_v = math.ceil(float(v))
        except (ValueError, TypeError):
            raise ValueError('ชั่วโมงจอดรถต้องเป็นตัวเลขครับ')
        
        # 2. ลอจิกการกำหนดช่วงเวลา
        if rounded_v < cls.MIN_LIMIT:
            raise ValueError('เวลาจอดติดไม่ได้')
        if rounded_v > cls.MAX_LIMT:
            raise ValueError('ห้ามจอดเกิน 24 ชั่วโมง')
        return rounded_v
    

class FirstName(BaseModel):
    value: str

    @field_validator('value')
    @classmethod
    def not_empty(cls, v:str) -> str:

        fname = v.strip()
        if not fname.strip():
            raise ValueError('กรุณากรอกชื่อด้วยครับ')
        if len(fname) < 2:
            raise ValueError('ชื่อสั้งไปไหมครับ')
        return fname
    

class LastName(BaseModel):
    value: str

    @field_validator('value')
    @classmethod
    def not_empty(cls, v:str) -> str:

        lname = v.strip()
        if not lname:
            raise ValueError('กรุณากรอกนามสกุลด้วยครับ')
        if len(lname) < 2:
            raise ValueError('นามสกุลสั้งเกินไป')
        return lname
    

class MoneyTHB(BaseModel):
    value: float
    
    @field_validator('value')
    @classmethod
    def check_not_negative(cls, m:float) -> float:
        if m < 0:
            raise ValueError('เงินต้องไม่น้อยกว่าศูนย์')
        return m