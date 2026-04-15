import sys
import os

# ฝัง GPS ให้ Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager  # 🚩 1. นำเข้าเครื่องมือเปิด/ปิดร้านตัวใหม่
from fastapi import FastAPI, HTTPException
from uuid import UUID

from Hospital_System.domain.hospital_registry import HospitalRegistry


# 🚩 2. สร้างฟังก์ชัน Lifespan (วงจรชีวิตของ API)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- ส่วนนี้ทำงานตอน "เปิดเซิร์ฟเวอร์" (Startup) ---
    HospitalRegistry.queue_service()  # ปลุกผู้อำนวยการ
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

# ใส่ไว้ล่างสุดของไฟล์ main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Hospital_System.api.main:app", host="127.0.0.1", port=8000, reload=True)