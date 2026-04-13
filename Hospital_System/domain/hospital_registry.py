# domain/hospital_registry.py
from typing import Optional

# --- โซนงานบริหาร (Domain Service): นำเข้าตัวพยาบาลและเจ้าหน้าที่ ---
from Hospital_System.domain.domain_service.patient_registrar import PatientRegistrar
from Hospital_System.domain.domain_service.queue_service import QueueService
from Hospital_System.domain.interface.repository import QueueRecord

# --- โซนงานช่าง (Infrastructure): นำเข้าตู้เก็บของจริง ---
from Hospital_System.infrastructure.sqlite_patient_repository import SqlPatientRecord
from Hospital_System.infrastructure.sqlite_queue_repository import SqlQueueRepository


class HospitalRegistry:
    """
    HospitalRegistry: เปรียบเหมือน "ผู้อำนวยการโรงพยาบาล"
    หน้าที่: ใครอยากได้อะไร ให้มาขอที่นี่ ผู้อำนวยการจะจัดของที่ถูกต้องไปให้เอง
    """

    # 1. กำหนดชื่อไฟล์ฐานข้อมูลไว้ที่เดียว (ถ้าจะเปลี่ยนชื่อไฟล์ แก้ตรงนี้ที่เดียวจบ)
    _DB_PATH = r"hospital_database.db"

    # 2. พื้นที่เก็บของส่วนตัวของผู้อำนวยการ (จำว่าเคยสร้างใครไว้บ้างหรือยัง)
    _queue_service: Optional[QueueService] = None
    _patient_registrar: Optional[PatientRegistrar] = None

    @classmethod
    def configure_queue(cls, queue_repo: QueueRecord) -> None:
        cls._queue_service = QueueService(repo=queue_repo)

    @classmethod
    def queue_service(cls) -> QueueService | None:
        if cls._queue_service is None:
            repo = SqlQueueRepository(db_path=cls._DB_PATH)
            cls._queue_service = QueueService(repo=repo)
        return cls._queue_service

    @classmethod
    def reset(cls):
        """ล้างสมองผู้อำนวยการ: ให้ลืมทุกคนที่เคยจ้างมา (จำเป็นมากตอนรันเทสหลายๆ รอบ)"""
        cls._patient_registrar = None
        cls._queue_service = None

    @classmethod
    def patient_registrar(cls) -> PatientRegistrar | None:
        """เมธอดเบิกตัว 'พยาบาลทะเบียน'"""

        # เช็คในใจก่อนว่า: "เราเคยจ้างพยาบาลคนนี้มาหรือยัง?" (ถ้าเป็น None คือยังไม่มี)
        if cls._patient_registrar is None:
            # ก) ถ้ายังไม่มี... ผู้อำนวยการจะไปเบิก 'ตู้เหล็กเก็บข้อมูลคนไข้' (SQLite Repo) มาก่อน
            repo = SqlPatientRecord(db_path=cls._DB_PATH)

            # ข) จากนั้น 'จ้างพยาบาล' (สร้าง Registrar) แล้วยื่นตู้เหล็กให้พยาบาลถือไว้ทำงาน
            cls._patient_registrar = PatientRegistrar(repo=repo)

        # ค) ส่งตัวพยาบาลที่พร้อมทำงาน (มีตู้เหล็กในมือแล้ว) กลับไปให้คนที่เรียกใช้
        return cls._patient_registrar

