# domain_service.py
from uuid import UUID
from typing import Tuple

from datetime import datetime, date

from Hospital_System.domain.custom_error import DuplicationQueueError
from Hospital_System.domain.entities import Queue
from Hospital_System.domain.repository import QueueRecord
from Hospital_System.domain.value_object import Number, VitalSigns, QueueStatus, Diagnosis


class QueueService:
    def __init__(self, repo: QueueRecord) -> None:
        self.repo = repo

    def issue_new_queue(self, patient_id: UUID, today:date, vital_signs:VitalSigns) -> Queue:
        self._ensure_no_duplicate_queue(patient_id, today)

        last_queue = self.repo.get_last_queue()
        last_num = last_queue.queue_number if last_queue else Number(id=0)
        last_date = last_queue.queue_date if last_queue else date(1990, 1, 1)

        next_num, next_date, _ = self.get_next_number(
            last_number=last_num, last_date=last_date, today=today, time_now=datetime.now())

        new_queue = Queue(
            patient_id=patient_id,
            queue_number=next_num,
            queue_date=next_date,
            vital_signs=vital_signs,
            status=QueueStatus.WAITING
        )
        self.repo.save(new_queue)

        return new_queue

    def get_next_number(self, last_number:Number, last_date: date, time_now: datetime, today: date) -> Tuple[Number,date, datetime]:
        last_number, last_date = self._reset_date_and_number(last_number, last_date, today)
        now_number = Number(id=last_number.id + 1)
        return now_number, last_date, time_now

    def start_consultation(self, queue_id:UUID) -> Queue:
        queue = self.repo.get_by_queue_id(queue_id=queue_id)
        self._check_none_type(queue, queue_id)
        queue.start_consultation()
        self.repo.save(queue)
        return queue

    def complete_visit(self, queue_id: UUID, diagnosis: Diagnosis) -> Queue:
        queue = self.repo.get_by_queue_id(queue_id=queue_id)
        self._check_none_type(queue, queue_id)
        queue.complete_visit(diagnosis)
        self.repo.save(queue)
        return queue


    def _check_none_type(self, queue: Queue | None, queue_id: UUID):
        if queue is None:
            raise ValueError(f'ไม่พบใบคิวรหัส {queue_id} ในระบบครับ')

    def _ensure_no_duplicate_queue(self, patient_id: UUID, today: date):
        existing_queue = self.repo.find_active_queue_by_patient(patient_id=patient_id, queue_date=today)
        if existing_queue:
            raise DuplicationQueueError(f'คนไข้ ID {patient_id} จองคิวซ้ำไม่ได้ครับ')

    def _reset_date_and_number(self, last_number: Number, last_date: date, today: date) -> tuple[Number, date]:
        if last_date < today:
            last_date = today
            last_number = Number(id=0)
        return last_number, last_date