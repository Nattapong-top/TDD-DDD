from pydantic import BaseModel, field_validator
class ParkingHour(BaseModel):
    value:int

    @field_validator('value')
    @classmethod
    def check_range(cls, v):
        '''กำหนดชั่วโมง ไม่น้อยกว่า 0 ไม่เกิน 24'''
        if v < 0:
            raise ValueError('เวลาจอดติดไม่ได้')
        if v > 24:
            raise ValueError('ห้ามจอดเกิน 24 ชั่วโมง')
        return v