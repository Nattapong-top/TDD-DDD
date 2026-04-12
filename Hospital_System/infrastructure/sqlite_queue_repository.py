import json
import sqlite3
from contextlib import closing
from datetime import date
from uuid import UUID

from Hospital_System.domain.domain_service.queue_service import Queue
from Hospital_System.domain.interface.repository import QueueRecord
from Hospital_System.domain.value_object import (
    QueueStatus, Version, VitalSigns, BloodPressure, Weight, Height,
    Temperature, Number, MedicineInfo, Diagnosis
)


class SqlQueueRepository(QueueRecord):
    # =====================================================================
    # 1. SQL CONSTANTS (ศูนย์รวมคำสั่ง DB ทั้งหมดอยู่ที่นี่ที่เดียว)
    # =====================================================================
    _CREATE_SCHEMA_QUERY = '''
        CREATE TABLE IF NOT EXISTS queue (
            q_id TEXT PRIMARY KEY, p_id TEXT NOT NULL, p_num INTEGER NOT NULL,
            q_date TEXT NOT NULL, status TEXT NOT NULL, ver INTEGER NOT NULL,
            bp_sys INTEGER, bp_dia INTEGER, w_kg REAL, h_cm REAL, temp_c REAL,
            symptom TEXT, diag_disease TEXT, diag_treatment TEXT, diag_meds TEXT
        )
    '''

    _UPSERT_QUEUE_QUERY = '''
        INSERT OR REPLACE INTO queue
        (q_id, p_id, p_num, q_date, status, ver, bp_sys, bp_dia, 
        w_kg, h_cm, temp_c, symptom, diag_disease, diag_treatment, diag_meds)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    _SELECT_BY_ID_QUERY = 'SELECT * FROM queue WHERE q_id = ?'
    _SELECT_ALL_QUERY = 'SELECT * FROM queue'

    # =====================================================================
    # 2. CORE METHODS (สั้น กระชับ อ่านปรู๊ดเดียวรู้เรื่อง)
    # =====================================================================
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_schema(self) -> None:
        with closing(self._get_connection()) as conn:
            with conn:
                conn.execute(self._CREATE_SCHEMA_QUERY)

    def save(self, queue: Queue) -> None:
        """เปิดประตู -> แปลงของลงกล่อง -> ยัดใส่ DB"""
        with closing(self._get_connection()) as conn:
            with conn:
                diag_data = self._prepare_diagnosis(queue)
                # โยนหน้าที่สร้าง Tuple 15 ตัวไปให้ Helper จบปิ๊ง!
                data_tuple = self._map_entity_to_tuple(queue, diag_data)
                conn.execute(self._UPSERT_QUEUE_QUERY, data_tuple)

    def get_by_queue_id(self, queue_id: UUID) -> Queue | None:
        with closing(self._get_connection()) as conn:
            row = conn.execute(self._SELECT_BY_ID_QUERY, (str(queue_id),)).fetchone()
            if not row:
                return None
            return self._map_row_to_entity(row)

    def get_all(self) -> list[Queue]:
        with closing(self._get_connection()) as conn:
            rows = conn.execute(self._SELECT_ALL_QUERY).fetchall()
            return [self._map_row_to_entity(row) for row in rows]

    def get_last_queue(self) -> Queue | None:
        raise NotImplementedError('เดี๋ยวป๋ามาเขียน SQL ทีหลังครับ')

    def find_active_queue_by_patient(self, patient_id: UUID, queue_date: date) -> Queue | None:
        raise NotImplementedError('เดี๋ยวป๋ามาเขียน SQL ทีหลังครับ')

    # =====================================================================
    # 3. HELPER METHODS (ลูกมือรับจบงานถึกทน)
    # =====================================================================
    def _prepare_diagnosis(self, queue: Queue) -> dict[str, str | None]:
        if not queue.diagnosis:
            return {"disease": None, "treatment": None, "meds": None}

        return {
            "disease": queue.diagnosis.disease,
            "treatment": queue.diagnosis.treatment,
            "meds": json.dumps([m.model_dump() for m in queue.diagnosis.medicine_prescribed])
        }

    def _map_entity_to_tuple(self, queue: Queue, diag_data: dict) -> tuple:
        """แปลง Object เป็น Tuple เพื่อส่งให้ SQLite"""
        return (
            str(queue.id), str(queue.patient_id), queue.queue_number.id,
            queue.queue_date.isoformat(), queue.status.value, queue.version.number,
            queue.vital_signs.blood_pressure.systolic, queue.vital_signs.blood_pressure.diastolic,
            queue.vital_signs.weight.value, queue.vital_signs.height.value,
            queue.vital_signs.temperature.value, queue.vital_signs.symptom,
            diag_data["disease"], diag_data["treatment"], diag_data["meds"]
        )

    def _map_row_to_entity(self, row: sqlite3.Row) -> Queue:
        """แปลง Row จาก SQLite คืนเป็น Object"""
        diagnosis_obj = None
        if row['diag_disease']:
            meds_data = json.loads(row['diag_meds']) if row['diag_meds'] else []
            meds = [MedicineInfo(**m) for m in meds_data]
            diagnosis_obj = Diagnosis(
                disease=row['diag_disease'], treatment=row['diag_treatment'], medicine_prescribed=meds,
            )

        return Queue(
            id=UUID(row['q_id']), patient_id=UUID(row['p_id']), queue_number=Number(id=row['p_num']),
            queue_date=date.fromisoformat(row['q_date']), status=QueueStatus(row['status']),
            version=Version(number=row['ver']), vital_signs=VitalSigns(
                blood_pressure=BloodPressure(systolic=row['bp_sys'], diastolic=row['bp_dia']),
                weight=Weight(value=row['w_kg']), height=Height(value=row['h_cm']),
                temperature=Temperature(value=row['temp_c']), symptom=row['symptom']
            ),
            diagnosis=diagnosis_obj
        )