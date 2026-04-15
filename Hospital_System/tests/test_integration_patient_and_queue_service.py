from datetime import date

from pytest import raises

from Hospital_System.domain.custom_error import InvalidCancelRequestError
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


def test_doctor_starts_consultation_should_change_status_to_IN_PROGRESS(new_patient, queue_service):
    # --- 1. เตรียมของ (Arrange) ---
    # ดึงคิวที่เพิ่งสร้างตอนลงทะเบียนมาดู (มันควรจะเป็นสถานะ WAITING)
    active_queue = queue_service.get_active_queue_by_patient(new_patient.id)
    assert active_queue.status == QueueStatus.WAITING

    # --- 2. ลงมือทำ (Act) ---
    # หมอกดปุ่มเรียกคิวเข้าห้องตรวจ
    updated_queue = queue_service.start_consultation(queue_id=active_queue.id)
    assert updated_queue.status == QueueStatus.IN_PROGRESS

    # 🚩 พิสูจน์ความชัวร์: ไปแอบเปิดตู้เหล็กดูอีกรอบ ว่าในฐานข้อมูลมันเปลี่ยนจริงๆ ไหม!
    db_queue = queue_service.get_active_queue_by_patient(updated_queue.patient_id)
    assert db_queue.status == QueueStatus.IN_PROGRESS
    assert db_queue.version.number == 2


def test_doctor_complete_visit_should_change_status_to_COMPLETE(new_patient, queue_service, diagnosis):
    # --- 1. เตรียมของ (Arrange) ---
    # ดึงคิวที่เพิ่งสร้างตอนลงทะเบียนมาดู (มันควรจะเป็นสถานะ WAITING)
    active_queue = queue_service.get_active_queue_by_patient(new_patient.id)
    assert active_queue.status == QueueStatus.WAITING

    # --- 2. ลงมือทำ (Act) ---
    # หมอกดปุ่มเรียกคิวเข้าห้องตรวจ
    updated_queue = queue_service.start_consultation(queue_id=active_queue.id)
    assert updated_queue.status == QueueStatus.IN_PROGRESS

    completed_queue = queue_service.complete_visit(updated_queue.id,diagnosis)
    assert completed_queue.status == QueueStatus.COMPLETED
    assert completed_queue.version.number == 3


    # 🚩 พิสูจน์ความชัวร์: ไปแอบเปิดตู้เหล็กดูอีกรอบ ว่าในฐานข้อมูลมันเปลี่ยนจริงๆ ไหม!
    db_queue = queue_service.repo.get_by_queue_id(completed_queue.id)
    assert db_queue.status == QueueStatus.COMPLETED
    assert db_queue.version.number == 3

def test_doctor_cancel_visit_should_change_status_to_CANCELLED(new_patient, queue_service):
    active_queue = queue_service.get_active_queue_by_patient(new_patient.id)
    assert active_queue.status == QueueStatus.WAITING
    assert active_queue.version.number == 1

    cancelled_queue = queue_service.cancel_visit(active_queue.id)
    assert cancelled_queue.status == QueueStatus.CANCELLED
    assert cancelled_queue.version.number == 2

    db_queue = queue_service.repo.get_by_queue_id(cancelled_queue.id)
    assert db_queue.status == QueueStatus.CANCELLED



def test_doctor_cancel_visit_should_change_status_to_CANCELLED_when_status_IN_PROGRESS(new_patient, queue_service):
    active_queue = queue_service.get_active_queue_by_patient(new_patient.id)
    assert active_queue.status == QueueStatus.WAITING
    assert active_queue.version.number == 1

    in_progress_queue = queue_service.start_consultation(active_queue.id)
    db_active = queue_service.get_active_queue_by_patient(in_progress_queue.patient_id)
    assert db_active.status == QueueStatus.IN_PROGRESS

    cancelled_queue = queue_service.cancel_visit(in_progress_queue.id)
    assert cancelled_queue.status == QueueStatus.CANCELLED
    assert cancelled_queue.version.number == 3

    db_queue = queue_service.repo.get_by_queue_id(cancelled_queue.id)
    assert db_queue.status == QueueStatus.CANCELLED
    assert db_queue.version.number == 3

def test_doctor_cannot_cancel_visit_should_raise_error_when_status_COMPLETE(new_patient, queue_service, diagnosis):
    # --- 1. เตรียมของ (Arrange) ---
    # ดึงคิวที่เพิ่งสร้างตอนลงทะเบียนมาดู (มันควรจะเป็นสถานะ WAITING)
    active_queue = queue_service.get_active_queue_by_patient(new_patient.id)
    assert active_queue.status == QueueStatus.WAITING

    # --- 2. ลงมือทำ (Act) ---
    # หมอกดปุ่มเรียกคิวเข้าห้องตรวจ
    updated_queue = queue_service.start_consultation(queue_id=active_queue.id)
    assert updated_queue.status == QueueStatus.IN_PROGRESS

    completed_queue = queue_service.complete_visit(updated_queue.id,diagnosis)
    assert completed_queue.status == QueueStatus.COMPLETED
    assert completed_queue.version.number == 3


    # 🚩 พิสูจน์ความชัวร์: ไปแอบเปิดตู้เหล็กดูอีกรอบ ว่าในฐานข้อมูลมันเปลี่ยนจริงๆ ไหม!
    db_queue = queue_service.repo.get_by_queue_id(completed_queue.id)
    assert db_queue.status == QueueStatus.COMPLETED
    assert db_queue.version.number == 3

    with raises(InvalidCancelRequestError) as error:
        queue_service.cancel_visit(completed_queue.id)

    assert 'ไม่สามารถยกเลิกการตรวจได้ เพราะสถานะปัจจุบันคือ' in str(error.value)