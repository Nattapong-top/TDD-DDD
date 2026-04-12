from abc import ABC, abstractmethod
from datetime import date
from typing import Optional
from uuid import UUID

from Hospital_System.domain.entities import Queue, Patient
from Hospital_System.domain.value_object import NationalID


class QueueRecord(ABC):
    @abstractmethod
    def get_last_queue(self) -> Optional[Queue]:
        pass

    @abstractmethod
    def save(self, queue: Queue) -> None:
        pass

    @abstractmethod
    def find_active_queue_by_patient(self, patient_id: UUID, queue_date: date) -> Optional[Queue]:
        pass

    @abstractmethod
    def get_by_queue_id(self, queue_id: UUID) -> Optional[Queue]:
        pass


class PatientRecord(ABC):
    @abstractmethod
    def save(self, patient: Patient) -> None:
        """บันทึกหรืออัปเดตข้อมูลคนไข้"""
        pass

    @abstractmethod
    def get_by_national_id(self, national_id: NationalID) -> Optional[Patient]:
        """หาคนไข้จากเลขบัตรประชาชน"""
        pass

