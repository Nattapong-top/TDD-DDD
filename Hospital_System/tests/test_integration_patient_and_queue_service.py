from datetime import date

from Hospital_System.domain.domain_service import queue_service
from Hospital_System.domain.value_object import QueueStatus, Name, NationalID, PhoneNumber, DateOfBirth, Rights, \
    PatientRights


def test_register_new_patient_should_auto_create_queue(
        queue_service, new_patient):
    active_queue = queue_service.get_active_queue_by_patient(new_patient.id)
    assert active_queue is not None
    assert active_queue.patient_id == new_patient.id
    assert active_queue.status == QueueStatus.WAITING


def test_register_new_patient_should_registration_date_parameter(
        registrar, registered_address, vital_signs, current_address, queue_service):
    future_date = date(2027, 1, 1)
    new_patient = registrar.register_new_patient(
        national_id=NationalID(id='1234567890123'),
        first_name=Name(value='นนทพัฒน์'),
        last_name=Name(value='คนสุขภาพดี'),
        phone_number=PhoneNumber(value='0123456789'),
        date_of_birth=DateOfBirth(year=1990, month=12, day=31),
        registered_address=registered_address,
        current_address=current_address,
        rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY),
        vital_signs=vital_signs,
        registration_date=future_date
    )
    active_queue = queue_service.get_active_queue_by_patient(
        patient_id=new_patient.id,
        search_date=future_date)
    assert active_queue is not None
    assert active_queue.patient_id == new_patient.id
    assert active_queue.queue_date == future_date