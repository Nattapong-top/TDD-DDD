from abc import ABC, abstractmethod
from datetime import date
from typing import Optional
from uuid import UUID

from Hospital_System.domain.entities import Queue


class QueueRecord(ABC):
    @abstractmethod
    def get_last_queue(self) -> Optional[Queue]:
        pass

    @abstractmethod
    def save(self, queue: Queue) -> None:
        pass

    @abstractmethod
    def update(self, queue: Queue) -> None:
        pass

    @abstractmethod
    def find_active_queue_by_patient(self, patient_id: UUID, queue_date: date) -> Optional[Queue]:
        pass

    @abstractmethod
    def get_by_queue_id(self, queue_id: UUID) -> Optional[Queue]:
        pass
