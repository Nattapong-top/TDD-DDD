#Hospital_System.domain.domain_service.patient_registrar

from datetime import date
from uuid import uuid4

from Hospital_System.domain.custom_error import DuplicateNationalIDError
from Hospital_System.domain.entities import Patient
from Hospital_System.domain.value_object import (
    NationalID, Name, PhoneNumber, DateOfBirth, Address, Rights, VitalSigns)


class PatientRegistrar:
    def __init__(self,repo, queue_service) -> None:
        self.repo = repo
        self.queue_service = queue_service

    def register_new_patient(self,
                             national_id: NationalID, first_name: Name, last_name: Name,
                             phone_number: PhoneNumber, date_of_birth: DateOfBirth,
                             registered_address: Address, current_address: Address,
                             rights: Rights, vital_signs: VitalSigns,
                             registration_date: date = None) -> Patient:

        today = registration_date or date.today()

        self._check_duplicate_national_id(national_id)

        new_patient = Patient(
            id=uuid4(),
            national_id=national_id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            registered_address=registered_address,
            current_address=current_address,
            rights=rights
        )

        self._save_patient(new_patient)
        self.queue_service.issue_new_queue(
            patient_id=new_patient.id,
            today=today, # หนี้เก่า ว่างจะเคลียร์
            vital_signs=vital_signs
        )
        return new_patient

    def update_patient_info(self, patient: Patient) -> None:
        self.repo.update(patient=patient)


    def _check_duplicate_national_id(self, national_id: NationalID):
        existing_patient = self.repo.get_by_national_id(national_id=national_id)
        if existing_patient:
            raise DuplicateNationalIDError(f'เลขบัตรประชาชนนี้มีในระบบแล้ว: {national_id.id}')

    def _save_patient(self, patient: Patient) -> Patient:
        self.repo.save(patient=patient)
        return patient