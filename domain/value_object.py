from pydantic import BaseModel, field_validator
import math


class ParkingHour(BaseModel):
    value:int

    @field_validator('value', mode='before')
    @classmethod
    def round_up_and_check_range(cls, v):
        '''กำหนดชั่วโมงปัดเศษขึ้นและ ไม่น้อยกว่า 0 ไม่เกิน 24'''
        # 1. ลอจิกการปัดเศษ: ใช้สูตรคณิตศาสตร์
        v = math.ceil(v)

        # 2. ลอจิกการกำหนดช่วงเวลา
        if v < 0:
            raise ValueError('เวลาจอดติดไม่ได้')
        if v > 24:
            raise ValueError('ห้ามจอดเกิน 24 ชั่วโมง')
        return v