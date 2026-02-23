from pydantic import BaseModel, field_validator, ConfigDict
import math
from typing import Any, ClassVar
import logging

# ต้องรันบรรทัดนี้ "ก่อน" ที่จะมีการเรียกใช้ logging.info/error ครั้งแรกนะครับป๋า
logging.basicConfig(
    level=logging.INFO,  # บอกยามว่า "เอาตั้งแต่ระดับ INFO ขึ้นไปนะ"
    format='%(asctime)s - %(levelname)s - %(message)s' # ปรับหน้าตาให้ดูโปร
)


class ParkingHour(BaseModel):
    # แช่แข็ง Object ห้ามใครแก้ค่าหลังสร้างเสร็จ
    model_config = ConfigDict(frozen=True)
    value:int

    # ใส่ ClassVar[ประเภท] คลุมไว้ เพื่อบอกว่าเป็น "กฎส่วนกลาง"
    MIN_LIMIT: ClassVar[int] = 0
    MAX_LIMIT: ClassVar[int] = 24
    FEE_FREE: ClassVar[float] = 0.25

    @field_validator('value', mode='before')
    @classmethod
    def round_up_and_check_range(cls, v:Any) -> int:
        '''กำหนดชั่วโมงปัดเศษขึ้นและ ไม่น้อยกว่า 0 ไม่เกิน 24'''
        # 1. ลอจิกการปัดเศษ: ใช้สูตรคณิตศาสตร์
        try:
            val_float = float(v)
        except (ValueError, TypeError) as e:
            # ถ้าพัง จด ERROR พร้อมหลักฐาน (e) ทันที!
            logging.error(f"ป๋าครับ! มีคนกรอกของเสียเข้ามา: '{v}' | รายละเอียด: '{e}'")
            raise ValueError('ชั่วโมงจอดรถต้องเป็นตัวเลขครับ')

        # 2. ลอจิกการกำหนดช่วงเวลา
        if val_float < cls.MIN_LIMIT or val_float > cls.MAX_LIMIT:
            logging.warning(f"กรอกเลขเกินช่วงที่กำหนด: {val_float}")
            raise ValueError(f'ห้ามจอดน้อยกว่า {cls.MIN_LIMIT} หรือเกิน {cls.MAX_LIMIT} ชม.')

        if val_float <= cls.FEE_FREE :
            logging.info(f"รับข้อมูลชั่วโมงจอด: {val_float} -> ปัดเศษลงเป็น: {0}")
            return 0
            
        rounded_v = math.ceil(val_float)
        # ถ้าผ่าน จด INFO ไว้หน่อยก็ได้ป๋า
        logging.info(f"รับข้อมูลชั่วโมงจอด: {v} -> ปัดเศษเป็น: {rounded_v}")
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
    # 1. แช่แข็ง Object ห้ามใครแก้ค่าเงินหลังจากสร้างเสร็จแล้ว
    model_config = ConfigDict(frozen=True)
    value: float

    # 2. ตั้งกฎขั้นต่ำไว้ที่บอร์ดกลาง (Class Variable)
    MIN_AMOUNT: ClassVar[float] = 0.0
    
    @field_validator('value', mode='before')
    @classmethod
    def check_not_negative(cls, v:Any) -> float:
        """ตรวจสอบว่าจำนวนเงินต้องเป็นตัวเลขและไม่ติดลบ"""
        # 3. รับของมาเป็น Any แล้วลองแปลงร่างเป็นเลขทศนิยม
        try:
            val = float(v)
        except (ValueError, TabError):
            raise ValueError('จำนวนเงินต้องเป็นตัวเลขเท่านั้นครับ')
        
        if val < cls.MIN_AMOUNT:
            raise ValueError(f'เงินต้องไม่น้อยกว่า {cls.MIN_AMOUNT} บาทครับ')
        return val