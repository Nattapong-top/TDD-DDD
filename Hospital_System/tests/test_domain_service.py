# test_domain_service.py
import uuid
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pytest import fixture, raises

from Hospital_System.domain.custom_error import DuplicationQueueError
from Hospital_System.domain.domain_service import QueueService
from Hospital_System.domain.entities import Queue, Patient
from Hospital_System.domain.repository import QueueRecord
from Hospital_System.domain.value_object import (
    Number, VitalSigns, BloodPressure, Weight, Height, Temperature,
    QueueStatus, Rights, PatientRights, Province, Address, DateOfBirth,
    PhoneNumber, Name, NationalID)


@fixture
def today_date() -> date:
    return date(2026, 3, 28)

@fixture
def now() -> datetime:
    return datetime(2026, 3, 28,
                    22, 43, 53, 302903)

@fixture
def repo() -> QueueRecord:
    return FakeQueueRecord()

@fixture
def queue_service(repo) -> QueueService:
    return QueueService(repo)

@fixture
def queue(patient):
    return Queue(
        patient_id=patient.id,
        queue_number=Number(id=1),
        queue_date=date.today(),
        vital_signs=VitalSigns(
            blood_pressure=BloodPressure(systolic=120, diastolic=80),
            weight=Weight(value=80),
            height=Height(value=177),
            temperature=Temperature(value=39.0),
            symptom='น้ำหมูกไหล ปวดหัว ตัวร้อน หนาวสั่น'
        ),
        status=QueueStatus.WAITING
    )

@fixture
def vital_signs():
    return VitalSigns(
    blood_pressure=BloodPressure(systolic=120, diastolic=80),
    weight=Weight(value=80),
    height=Height(value=177),
    temperature=Temperature(value=39.0),
    symptom='น้ำหมูกไหล ปวดหัว ตัวร้อน หนาวสั่น'
)

@fixture
def patient():
    return Patient(
        id=uuid.uuid4(),
        nation_id=NationalID(id='1234567890123'),
        first_name=Name(value='นนทพัฒน์'),
        last_name=Name(value='คนสุขภาพดี'),
        phone_number=PhoneNumber(value='0123456789'),
        date_of_birth=DateOfBirth(year=1990, month=12, day=31),
        registered_address=Address(
            house_number='10',
            street='วิวิธสุรการ',
            sub_district='มุกดาหาร',
            district='เมือง',
            province=Province.MUKDAHAN,
            postal_code='49000'
        ),
        current_address=Address(  # ตั้งอยู่ที่ 173 ถนนดินสอ แขวงเสาชิงช้า เขตพระนคร กรุงเทพมหานคร 10200
            house_number='173',
            street='ดินสอ',
            sub_district='เสาชิงช้า',
            district='พระนคร',
            province=Province.BANGKOK,
            postal_code='10200'
        ),
        rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY)
    )


class FakeQueueRecord(QueueRecord):
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


def test_should_queue_service_issue_first_number_of_the_day(repo):
    service = QueueService(repo)

    today = date(2026, 3, 28)
    now = datetime(2026, 3, 28, 22, 43, 53, 302903)
    next_number, last_date, time_now = service.get_next_number(
        last_number=Number(id=0), last_date=today, time_now=now, today=today)
    assert next_number == Number(id=1)
    assert last_date == date(2026, 3, 28)
    assert time_now == datetime(2026, 3, 28, 22, 43, 53, 302903)

def test_should_queue_service_reset_number_and_last_date(repo, today_date, now):
    service = QueueService(repo)
    next_number, last_date, time_now = service.get_next_number(
        last_number=Number(id=99), last_date=date(2026, 3, 27),
        time_now=now, today=today_date)
    assert next_number == Number(id=1)
    assert last_date == today_date
    assert time_now == now


def test_should_queue_service_issue_first_queue_successfully(repo, queue_service, patient, vital_signs, today_date):
    new_queue = queue_service.issue_new_queue(
        patient_id=patient.id,
        today=today_date,
        vital_signs=vital_signs,
    )
    assert new_queue.queue_number == Number(id=1)
    assert new_queue.queue_date == date(2026, 3, 28)
    assert len(repo.queues) == 1

def test_should_queue_service_raise_error_duplication_queue(repo, queue_service, patient, vital_signs, today_date):
    new_queue = queue_service.issue_new_queue(
        patient_id=patient.id,
        today=today_date,
        vital_signs=vital_signs,
    )
    with raises(DuplicationQueueError) as excinfo:
        queue_service.issue_new_queue(
            patient_id=patient.id,
            today=today_date,
            vital_signs=vital_signs,
        )
    assert 'จองคิวซ้ำไม่ได้' in str(excinfo.value)