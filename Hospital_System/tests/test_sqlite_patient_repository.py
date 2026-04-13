import os
import uuid

from pytest import fixture, raises

from Hospital_System.domain.custom_error import DuplicateNationalIDError
from Hospital_System.domain.entities import Patient
from Hospital_System.domain.value_object import (
    NationalID, Name, PhoneNumber, DateOfBirth,
    Address, Province, Rights, PatientRights)
from Hospital_System.infrastructure.sqlite_patient_repository import SqlPatientRepository


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
    """เตรียมไฟล์ DB สำหรับเทสและลบทิ้งเมื่อเทสเสร็จ"""
    db_path = 'test_sqlite_patient_repository.db'
    if os.path.exists(db_path): os.remove(db_path)

    yield db_path
    if os.path.exists(db_path): os.remove(db_path)


@fixture
def repo(test_db):
    """สร้าง Repository Instance สำหรับใช้ในเทส"""
    return SqlPatientRepository(db_path=test_db)

# --- Test Cases: ไล่บี้ตั้งแต่ปกติจนถึงเคสแปลกๆ ---
def test_sql_patient_repository_should_save_retrieve_patient_when_info_valid(repo, patient):
    """CASE 1: เซฟได้-ดึงได้ (Happy Path)"""
    repo.save(patient=patient)
    assert repo is not None

    retrieved = repo.get_by_national_id(national_id=patient.national_id)
    assert retrieved is not None
    assert retrieved.national_id == patient.national_id
    assert retrieved == patient # Entity ต้องหน้าตาเหมือนเดิมเป๊ะ


def test_sql_patient_repository_should_raise_error_when_duplicate_national_id(repo, patient):
    """CASE 2: ป้องกันเลขบัตรซ้ำ (Integrity Check)"""
    repo.save(patient=patient)

    # สร้างคนใหม่ (ID ใหม่) แต่ใช้เลขบัตรเดิม
    duplicate_patient = patient.model_copy(update={'id': uuid.uuid4()})

    with raises(DuplicateNationalIDError) as error:
        repo.save(patient=duplicate_patient)
    assert 'เลขบัตรประชาชนนี้มีในระบบแล้ว' in str(error.value)


def test_sql_patient_repository_should_return_none_when_patient_not_found(repo, patient):
    """CASE 3: คืนค่า None เมื่อหาคนไข้ไม่เจอ (Sad Path)"""
    not_found = repo.get_by_national_id(NationalID(id='0000000000000'))
    assert not_found is None


def test_sql_patient_repository_handle_special_characters_and_long_strings(repo, patient):
    """CASE 4: รองรับชื่อยาวและอักขระพิเศษ (Edge Case)"""
    complex_name = Name(value="สมชาย 'สายฟ้า' มหานคร-อัครสถาน & *")
    patient.first_name = complex_name

    # อัปเดตที่อยู่ผ่าน model_copy เพราะเป็น Frozen Instance
    new_address = patient.registered_address.model_copy(
        update= {'street': "ถนน ๑๒๓/๔๕๖ (พิเศษ) & * ^ % $ # @"}
    )
    patient.registered_address = new_address

    repo.save(patient=patient)
    assert repo is not None

    retrieved = repo.get_by_national_id(national_id=patient.national_id)
    assert retrieved.registered_address.street == new_address.street
    assert retrieved.first_name.value == complex_name.value

def test_sql_patient_repository_should_save_retrieve_patient_with_version(repo, patient):
    repo.save(patient=patient)
    retrieved = repo.get_by_national_id(patient.national_id)

    assert retrieved is not None
    assert retrieved == patient
    assert retrieved.version.number == 1

def test_sql_patient_repository_should_update_phone_number_and_increment_version(repo, patient):
    repo.save(patient=patient)
    new_phone = PhoneNumber(value='0999999999')

    patient.update_phone_number(new_phone)
    repo.update(patient=patient)

    updated = repo.get_by_national_id(national_id=patient.national_id)
    assert updated.phone_number.value == '0999999999'
    assert updated.version.number == 2

def test_sql_patient_repository_should_raise_error_when_concurrency_conflict(repo, patient):
    repo.save(patient=patient)

    nurse_a_view = repo.get_by_national_id(national_id=patient.national_id)
    nurse_b_view = repo.get_by_national_id(national_id=patient.national_id)

    nurse_a_view.update_first_name(Name(value="สมชาย 'สายฟ้า' มหานคร-อัครสถาน & *"))
    repo.update(nurse_a_view)

    nurse_b_view.update_first_name(Name(value="มหานครอัครสถาน"))

    with raises(RuntimeError) as error:
        repo.update(nurse_b_view)

    assert 'update' in str(error.value)