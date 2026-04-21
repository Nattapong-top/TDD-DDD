# Hospital_System.domain.interfaces
from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, List
from uuid import UUID

from Hospital_System.domain.entities import Queue, Patient
from Hospital_System.domain.value_object import NationalID

class QueueRecord(ABC):
    @abstractmethod
    def get_last_queue(self) -> Optional[Queue]:
        """ดึงคิวล่าสุดเพื่อเอามาออกเลขคิวถัดไป"""
        pass

    @abstractmethod
    def save(self, queue: Queue) -> None:
        """บันทึกคิวใหม่"""
        pass

    @abstractmethod
    def update(self, queue: Queue) -> None:
        """อัปเดตข้อมูลคิว (เช่น เปลี่ยนสถานะ)"""
        pass

    @abstractmethod
    def find_active_queue_by_patient(self, patient_id: UUID, queue_date: date) -> Optional[Queue]:
        """เช็คว่าคนไข้คนนี้มีคิวที่ยังตรวจไม่เสร็จในวันนี้ไหม"""
        pass

    @abstractmethod
    def get_by_queue_id(self, queue_id: UUID) -> Optional[Queue]:
        """หาคิวจาก ID"""
        pass

    @abstractmethod
    def get_all_queues_today(self, today: date) -> List[Queue]:
        """ดึงคิวทั้งหมดของวันนี้ (สำหรับพยาบาล)"""
        pass

class PatientRecord(ABC):
    @abstractmethod
    def save(self, patient: Patient) -> None:
        """บันทึกข้อมูลคนไข้ใหม่"""
        pass

    @abstractmethod
    def update(self, patient: Patient) -> None:
        """อัปเดตข้อมูลคนไข้"""
        pass

    @abstractmethod
    def get_by_national_id(self, national_id: NationalID) -> Optional[Patient]:
        """หาคนไข้จากเลขบัตรประชาชน"""
        pass