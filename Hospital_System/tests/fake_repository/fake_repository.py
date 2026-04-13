from Hospital_System.domain.entities import Patient
from Hospital_System.domain.interface.repository import PatientRecord
from Hospital_System.domain.value_object import NationalID


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