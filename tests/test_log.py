import logging

logging.basicConfig(
    level=logging.DEBUG, # ป๋าสั่งให้บันทึกทุกระดับตั้งแต่ DEBUG ขึ้นไป
    format='%(asctime)s - %(levelname)s - %(message)s' # รูปแบบ: เวลา - ระดับความรุนแรง - ข้อความ
)

# ลองทดสอบความดัง 5 ระดับ
logging.debug("ป๋าครับ อันนี้เอาไว้ดูค่าตัวแปร (ละเอียดสุด)")
logging.info("ระบบเริ่มทำงานแล้วครับ")
logging.warning("ระวัง! มีคนพยายามเข้าใช้งานโดยไม่ระบุตัวตน")
logging.error("เกิดข้อผิดพลาด! แย่แล้วป๋า")
logging.critical("ระบบพังพินาศ! ต้องรีบแก้ด่วน")