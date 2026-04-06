import sqlite3
from contextlib import closing
from datetime import date
from uuid import UUID

from Hospital_System.domain.domain_service import Queue
from Hospital_System.domain.value_object import (
    QueueStatus, Version, VitalSigns, BloodPressure, Weight, Height, \
    Temperature, Number)


class SqlQueueRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_schema(self):
        query = '''
        CREATE TABLE IF NOT EXISTS queue (
            q_id TEXT PRIMARY KEY,
            p_id TEXT NOT NULL,
            p_num INTEGER NOT NULL,
            q_date TEXT NOT NULL,
            status TEXT NOT NULL,
            ver INTEGER NOT NULL,
            bp_sys INTEGER,
            bp_dia INTEGER,
            w_kg REAL,
            h_cm REAL,
            temp_c REAL,
            symptom TEXT
    )
    '''
        with closing(self._get_connection()) as conn:
            conn.execute(query)

    def save(self, queue: Queue) -> None:
        with closing(self._get_connection()) as conn:
            with conn:
                query = '''
                INSERT OR REPLACE INTO queue
                (q_id, p_id, p_num, q_date, status, ver, bp_sys, bp_dia, w_kg, h_cm, temp_c, symptom)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''

                data = (
                    str(queue.id),
                    str(queue.patient_id),
                    queue.queue_number.id,
                    queue.queue_date.isoformat(),
                    queue.status.value,
                    queue.version.number,
                    queue.vital_signs.blood_pressure.systolic,
                    queue.vital_signs.blood_pressure.diastolic,
                    queue.vital_signs.weight.value,
                    queue.vital_signs.height.value,
                    queue.vital_signs.temperature.value,
                    queue.vital_signs.symptom
                )
                conn.execute(query, data)

    def get_by_id(self, queue_id: UUID) -> Queue | None:
        query = 'SELECT * FROM queue WHERE q_id = ?'
        with closing(self._get_connection()) as conn:
            row = conn.execute(query, (str(queue_id),)).fetchone()

            if not row:
                return None

            return Queue(
                id=UUID(row['q_id']),
                patient_id=UUID(row['p_id']),
                queue_number=Number(id=row['p_num']),
                queue_date=date.fromisoformat(row['q_date']),
                status=QueueStatus(row['status']),
                version=Version(number=row['ver']),
                vital_signs=VitalSigns(
                    blood_pressure=BloodPressure(systolic=row['bp_sys'], diastolic=row['bp_dia']),
                    weight=Weight(value=row['w_kg']),
                    height=Height(value=row['h_cm']),
                    temperature=Temperature(value=row['temp_c']),
                    symptom=row['symptom']
                )
            )

    def get_all(self) -> list[Queue]:
        with closing(self._get_connection()) as conn:
            rows = conn.execute('SELECT * FROM queue').fetchall()
            queues = []
            for row in rows:
                q = Queue(
                    id=UUID(row['q_id']),
                    patient_id=UUID(row['p_id']),
                    queue_number=Number(id=row['p_num']),
                    queue_date=date.fromisoformat(row['q_date']),
                    status=QueueStatus(row['status']),
                    version=Version(number=row['ver']),
                    vital_signs=VitalSigns(
                        blood_pressure=BloodPressure(systolic=row['bp_sys'], diastolic=row['bp_dia']),
                        weight=Weight(value=row['w_kg']),
                        height=Height(value=row['h_cm']),
                        temperature=Temperature(value=row['temp_c']),
                        symptom=row['symptom']
                    )
                )
                queues.append(q)
            return queues

