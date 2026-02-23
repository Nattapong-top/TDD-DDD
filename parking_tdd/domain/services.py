from domain.value_object import ParkingHour, MoneyTHB
import logging

class ParkingService:
    def calculate_fee(self, hour:ParkingHour, rate:MoneyTHB) -> MoneyTHB:
        '''คำนวณค่าจอดรถตามชั่วโมงและอัตราที่กำหนด'''
        total = hour.value * rate.value
        logging.info(f'คำนวณค่าจอด: {hour.value} ชม. x {rate.value} บาท')
        return MoneyTHB(value=total)