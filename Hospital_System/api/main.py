import sys
import os

# ฝัง GPS ให้ Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager  # 🚩 1. นำเข้าเครื่องมือเปิด/ปิดร้านตัวใหม่
from fastapi import FastAPI, HTTPException
from uuid import UUID

from Hospital_System.domain.hospital_registry import HospitalRegistry
from pydantic import BaseModel
from Hospital_System.domain.value_object import (
    NationalID, Name, PhoneNumber, DateOfBirth, Address, Province,
    Rights, PatientRights, VitalSigns, BloodPressure, Weight, Height, Temperature
)


# 🚩 2. สร้างฟังก์ชัน Lifespan (วงจรชีวิตของ API)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- ส่วนนี้ทำงานตอน "เปิดเซิร์ฟเวอร์" (Startup) ---
    HospitalRegistry.init_database()  # ปลุกผู้อำนวยการ
    HospitalRegistry.queue_service()
    print("🏥 ผู้อำนวยการจัดเตรียมระบบหลังบ้านพร้อมแล้ว!")

    yield  # รอรับแขกตรงนี้...

    # --- ส่วนนี้ทำงานตอน "ปิดเซิร์ฟเวอร์" (Shutdown) ---
    print("🔒 ปิดประตูโรงพยาบาล พักผ่อนครับป๋า!")


# 🚩 3. เอา lifespan ไปใส่ตอนสร้าง FastAPI
app = FastAPI(
    title="Hospital Queue API Paa Top IT",
    description="ระบบจัดการคิวโรงพยาบาลของป๋าท๊อป",
    version="1.0.0",
    lifespan=lifespan
)


# --- จุดรับบริการ (Endpoints) คงเดิมครับ ---

@app.get("/")
def health_check():
    return {"message": "API Online ปลอดภัยดีครับป๋า"}


@app.get("/api/queues/{queue_id}")
def get_queue_status(queue_id: UUID):
    """ส่ง ID คิวเข้ามา เพื่อดูสถานะล่าสุด"""
    qs = HospitalRegistry.queue_service()
    queue = qs.repo.get_by_queue_id(queue_id)

    if queue is None:
        raise HTTPException(status_code=404, detail="ไม่พบใบคิวนี้ในระบบครับ")

    return {
        "queue_id": str(queue.id),
        "patient_id": str(queue.patient_id),
        "status": queue.status.value,
        "queue_number": queue.queue_number.id,
        "queue_date": str(queue.queue_date),
        "version": queue.version.number
    }


# --- 1. สร้างตระกร้าตรวจรับของจากหน้าเว็บ (Pydantic Schema) ---
class RegisterRequest(BaseModel):
    national_id: str
    first_name: str
    last_name: str
    phone_number: str
    dob_year: int
    dob_month: int
    dob_day: int
    house_number: str
    street: str
    sub_district: str
    district: str
    province: Province
    postal_code: str
    rights_type: PatientRights
    systolic: int
    diastolic: int
    weight: float
    height: float
    temperature: float
    symptom: str


# --- 2. สร้าง API รับลงทะเบียน (POST) ---
@app.post("/api/patients/register")
def register_patient(request: RegisterRequest):
    """API สำหรับพยาบาลหน้าเคาน์เตอร์ลงทะเบียนคนไข้ใหม่ และออกคิวอัตโนมัติ"""

    # 1. เบิกตัวผู้อำนวยการมาจัดเตรียมเครื่องมือ
    registrar = HospitalRegistry.patient_registrar()

    # 2. 🚩 แปลงข้อมูลดิบ (JSON) ให้เป็นของหรูหรา (Value Objects) สไตล์ DDD!
    address = Address(
        house_number=request.house_number, street=request.street,
        sub_district=request.sub_district, district=request.district,
        province=request.province, postal_code=request.postal_code
    )
    vital_signs = VitalSigns(
        blood_pressure=BloodPressure(systolic=request.systolic, diastolic=request.diastolic),
        weight=Weight(value=request.weight), height=Height(value=request.height),
        temperature=Temperature(value=request.temperature), symptom=request.symptom
    )

    # 3. สั่งพยาบาลทะเบียนทำงาน (มันจะรันโค้ดเก่าที่เราเขียนไว้ทั้งหมด!)
    new_patient = registrar.register_new_patient(
        national_id=NationalID(id=request.national_id),
        first_name=Name(value=request.first_name),
        last_name=Name(value=request.last_name),
        phone_number=PhoneNumber(value=request.phone_number),
        date_of_birth=DateOfBirth(year=request.dob_year, month=request.dob_month, day=request.dob_day),
        registered_address=address,
        current_address=address,  # สมมติว่าที่อยู่ปัจจุบันตรงกับทะเบียนบ้านไปก่อน
        rights=Rights(rights_type=request.rights_type),
        vital_signs=vital_signs
    )

    # 4. ไปตามหาคิวที่พึ่งถูกสร้างอัตโนมัติ เพื่อส่งรหัสกลับไปให้หน้าเว็บ
    qs = HospitalRegistry.queue_service()
    active_queue = qs.get_active_queue_by_patient(new_patient.id)

    return {
        "message": "ลงทะเบียนสำเร็จ!",
        "queue_id": str(active_queue.id),
        "queue_number": active_queue.queue_number.id,
        "status": active_queue.status.value
    }










# ใส่ไว้ล่างสุดของไฟล์ main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Hospital_System.api.main:app", host="127.0.0.1", port=8000, reload=True)