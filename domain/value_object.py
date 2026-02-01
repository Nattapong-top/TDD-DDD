from pydantic import BaseModel 
class ParkingHour(BaseModel):
    '''คำนวณชั่วโมง ไม่น้อยกว่า 0 ไม่เกิน 24'''
    # value:int
    # if value < 0:
