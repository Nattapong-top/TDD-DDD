import os
import uuid
from datetime import date, datetime
from pytest import fixture

from Hospital_System.domain.domain_service.queue_service import QueueService
from Hospital_System.domain.entities import Patient, Queue
from Hospital_System.domain.value_object import (
    Address, Province, MedicineInfo, Diagnosis, Rights, PatientRights, \
    PhoneNumber, Name, DateOfBirth, NationalID, Temperature, Weight, Height,
    BloodPressure, VitalSigns, QueueStatus, \
    Number, Version)

from Hospital_System.domain.domain_service.patient_registrar import PatientRegistrar
from Hospital_System.infrastructure.sqlite_patient_repository import SqlPatientRepository
from Hospital_System.infrastructure.sqlite_queue_repository import SqlQueueRepository
from Hospital_System.tests.fake_repository.fake_repository import FakeQueueRecord


@fixture(autouse=True)
def clear_db():
    yield
    # 🚩 ลบไฟล์ DB ของคิวด้วยครับป๋า
    db_files = ['hospital_database.db', 'test_hospital.db']
    for f in db_files:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass


@fixture
def patient_repo() -> SqlPatientRepository:
    return SqlPatientRepository('hospital_database.db')

@fixture
def queue_repo(tmp_path):
    """สร้างตู้เก็บคิว (SQL) ชั่วคราวสำหรับการเทส"""
    db_path = str(tmp_path / "test_hospital.db")
    repo = SqlQueueRepository(db_path)
    repo.create_schema() # 🚩 สร้างตารางรอไว้เลย
    return repo


@fixture
def queue_service(queue_repo):
    return QueueService(repo=queue_repo)

@fixture
def registrar(patient_repo, queue_service) -> PatientRegistrar:
    return PatientRegistrar(repo=patient_repo, queue_service=queue_service)


@fixture
def registered_address() -> Address:
    return Address(
        house_number='10',
        street='วิวิธสุรการ',
        sub_district='มุกดาหาร',
        district='เมือง',
        province=Province.MUKDAHAN,
        postal_code='49000'
    )


@fixture
def current_address() -> Address:
    return Address(  # ตั้งอยู่ที่ 173 ถนนดินสอ แขวงเสาชิงช้า เขตพระนคร กรุงเทพมหานคร 10200
        house_number='173',
        street='ดินสอ',
        sub_district='เสาชิงช้า',
        district='พระนคร',
        province=Province.BANGKOK,
        postal_code='10200'
    )


@fixture
def today_date() -> date:
    return date(2026, 3, 28)


@fixture
def now() -> datetime:
    return datetime(2026, 3, 28,
                    22, 43, 53, 302903)


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
        national_id=NationalID(id='1234567890123'),
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
        rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY),
        version=Version(number=1)
    )


@fixture
def new_queue(queue_service, patient, vital_signs, today_date):
    return queue_service.issue_new_queue(
        patient_id=patient.id,
        today=today_date,
        vital_signs=vital_signs,
    )


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
        status=QueueStatus.WAITING,
        version=Version(number=1)
    )


@fixture
def diagnosis(patient):
    return Diagnosis(
        disease='ไข้หวัดใหญ่',
        treatment='พักผ่อนน ดิ่มน้ำมากๆ',
        medicine_prescribed=[MedicineInfo(
            name='Paracetamol',
            strength='500mg',
            frequency='วันละ 3 ครั้ง หลักอาหาร'
        )]
    )

@fixture
def new_patient(registrar, vital_signs):
    return registrar.register_new_patient(
        national_id=NationalID(id='1234567890123'),
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
        rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY),
        vital_signs=vital_signs
        )



@fixture
def fake_repo():
    return FakeQueueRecord()


@fixture
def queue_sql():
    return SqlQueueRepository(db_path='test.db')

