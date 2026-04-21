from abc import ABC
from datetime import date
from typing import List, Optional
from uuid import UUID

from Hospital_System.domain.entities import Patient, Queue
from Hospital_System.domain.interface.repository import PatientRecord, QueueRecord
from Hospital_System.domain.value_object import NationalID, QueueStatus


class FakePatientRecord(PatientRecord):
    def __init__(self) -> None:
        self.patients = {}

    def save(self, patient: Patient) -> None:
        self.patients[patient.id] = patient

    def get_by_national_id(self, national_id: NationalID) -> Patient | None:
        return next((p for p in self.patients.values() if p.national_id == national_id), None)

    def update(self, patient: Patient) -> None:
        pass

# เคสที่ 4: ระบบฐานข้อมูลมีปัญหา (Infrastructure Failure)
class BrokenPatientRecord(PatientRecord):
    def save(self, patient: Patient) -> None:
        raise RuntimeError('Database พัง save ไม่ได้')

    def get_by_national_id(self, national_id: NationalID) -> None:
        return None

    def update(self, patient: Patient) -> None:
        pass

class FakeQueueRecord(QueueRecord, ABC):
    def __init__(self):
        self.queues: List[Queue] = []

    def get_last_queue(self) -> Optional[Queue]:
        return self.queues[-1] if self.queues else None

    def save(self, queue: Queue) -> None:
        self.queues.append(queue)

    def find_active_queue_by_patient(self, patient_id: UUID, queue_date: date) -> Optional[Queue]:
        for queue in self.queues:
            if (queue.patient_id == patient_id and
                    queue.queue_date == queue_date and
                    queue.status in [QueueStatus.WAITING, QueueStatus.IN_PROGRESS]):
                return queue
        return None

    def get_by_queue_id(self, queue_id: UUID) -> Optional[Queue]:
        for queue in self.queues:
            if queue.id == queue_id:
                return queue
        return None

    def update(self, queue: Queue) -> None:
        pass

    def get_all_queues_today(self, queue_date: date) -> List[Queue]:
        pass