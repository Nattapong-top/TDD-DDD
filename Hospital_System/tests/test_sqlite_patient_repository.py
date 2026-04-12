import os
import uuid

from pytest import fixture, raises

from Hospital_System.domain.custom_error import DuplicateNationalIDError
from Hospital_System.domain.entities import Patient
from Hospital_System.domain.value_object import (
    NationalID, Name, PhoneNumber, DateOfBirth,
    Address, Province, Rights, PatientRights)
from Hospital_System.infrastructure.sqlite_patient_repository import SqlPatientRecord


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
        rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY)
    )


@fixture
def test_db():
    db_path = 'test_sqlite_patient_repository.db'
    if os.path.exists(db_path): os.remove(db_path)

    yield db_path
    if os.path.exists(db_path): os.remove(db_path)

@fixture
def repo(test_db):
    return SqlPatientRecord(db_path=test_db)



def test_sql_patient_record_should_save_retrieve_patient_when_info_valid(repo, patient):
    repo.save(patient=patient)
    assert repo is not None

    retrieved = repo.get_by_national_id(national_id=patient.national_id)
    assert retrieved is not None
    assert retrieved.national_id == patient.national_id
    assert retrieved == patient


