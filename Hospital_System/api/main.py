import sys
import os
from datetime import date
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from uuid import UUID
from pydantic import BaseModel

# ฝัง GPS ให้ Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Hospital_System.domain.hospital_registry import HospitalRegistry
from Hospital_System.domain.value_object import (
    NationalID, Name, PhoneNumber, DateOfBirth, Address, Province,
    Rights, PatientRights, VitalSigns, BloodPressure, Weight, Height, Temperature
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup: เปิดโรงพยาบาล ---
    HospitalRegistry.init_database()
    print("🏥 ระบบฐานข้อมูลและศูนย์บัญชาการพร้อมให้บริการ!")
    yield
    # --- Shutdown: ปิดโรงพยาบาล ---
    print("🔒 ปิดระบบเรียบร้อย พักผ่อนครับป๋า!")


app = FastAPI(
    title="Hospital Queue API - Paa Top IT",
    lifespan=lifespan
)


# --- ข้อมูลรับเข้า (Request Schema) ---
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


# --- จุดบริการ (Endpoints) ---

@app.get("/")
def health_check():
    return {"message": "API Online ปลอดภัยดีครับป๋า", "status": "Ready"}


# # 🚩 จุดที่ 1: ต้องเอา /today ไว้ข้างบน {queue_id} เสมอ!
# @app.get("/api/queues/today")
# def get_all_queues_today():
#     """เมนูสำหรับพยาบาล: ดูรายชื่อคิวทุกคนของวันนี้"""
#     qs = HospitalRegistry.queue_service()
#     queues = qs.repo.get_today_queues(date.today())
#
#     return [
#         {
#             "queue_number": q.queue_number.id,
#             "status": q.status.value,
#             "patient_id": str(q.patient_id),
#             "queue_id": str(q.id)
#         } for q in sorted(queues, key=lambda x: x.queue_number.id)
#     ]


@app.get("/api/queues/{queue_id}")
def get_queue_status(queue_id: UUID) -> dict:
    qs = HospitalRegistry.queue_service()
    queue = qs.repo.get_by_queue_id(queue_id)
    if not queue:
        raise HTTPException(status_code=404, detail="ไม่พบใบคิวนี้ในระบบ")

    return {
        "queue_id": str(queue.id),
        "status": queue.status.value,
        "queue_number": queue.queue_number.id
    }


@app.post("/api/patients/register")
def register_patient(request: RegisterRequest) -> dict:
    # 🚩 จุดที่ 2: ใช้ Try-Except เพื่อดักจับ Error จาก Domain (เช่น ID ซ้ำ)
    try:
        registrar = HospitalRegistry.patient_registrar()

        address = Address(
            house_number=request.house_number, street=request.street,
            sub_district=request.sub_district, district=request.district,
            province=request.province, postal_code=request.postal_code
        )

        new_patient = registrar.register_new_patient(
            national_id=NationalID(id=request.national_id),
            first_name=Name(value=request.first_name),
            last_name=Name(value=request.last_name),
            phone_number=PhoneNumber(value=request.phone_number),
            date_of_birth=DateOfBirth(year=request.dob_year, month=request.dob_month, day=request.dob_day),
            registered_address=address,
            current_address=address,
            rights=Rights(rights_type=request.rights_type)
        )


        active_queue = HospitalRegistry.patient_repo().get_by_national_id(new_patient.national_id)

        return {
            "message": "ลงทะเบียนสำเร็จ!",
            "national_id": str(active_queue.national_id.id),
            'first_name': str(new_patient.first_name.value)
        }

    except ValueError as e:
        # ถ้า National ID ซ้ำ หรือข้อมูลผิดกฎ Domain มันจะเด้งมาที่นี่
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # กันเหนียวเผื่อมี Error อื่นๆ
        raise HTTPException(status_code=500, detail="เกิดข้อผิดพลาดภายในระบบ")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("Hospital_System.api.main:app", host="127.0.0.1", port=8000, reload=True)