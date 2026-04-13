#tests.test_patient_registrar
import os

from pydantic import ValidationError
from pytest import fixture, raises

from Hospital_System.domain.custom_error import DuplicateNationalIDError
from Hospital_System.domain.domain_service.patient_registrar import PatientRegistrar
from Hospital_System.domain.hospital_registry import HospitalRegistry
from Hospital_System.domain.value_object import Address, Province, NationalID, Name, PhoneNumber, DateOfBirth, Rights, \
    PatientRights
from Hospital_System.infrastructure.sqlite_patient_repository import SqlPatientRepository
from Hospital_System.tests.fake_repository.fake_repository import (
    BrokenPatientRecord)


# --- 1. Fixture สำหรับการจัดการไฟล์ DB ในการเทส ---
@fixture(autouse=True)
def clear_registry():
    """ล้างค่าใน Registry ทุกครั้งก่อนและหลังเทสแต่ละเคส เพื่อไม่ให้ค่าค้าง"""
    HospitalRegistry.reset()
    yield
    HospitalRegistry.reset()
    # ลบไฟล์ DB ที่อาจจะเกิดขึ้นจากการเทส (ถ้ามี)
    if os.path.exists('hospital_database.db'):
        os.remove('hospital_database.db')


@fixture
def repo() -> SqlPatientRepository:
    return SqlPatientRepository('hospital_database.db')


@fixture
def registrar() -> PatientRegistrar:
    return HospitalRegistry.patient_registrar()


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


def test_registrar_patient_when_patient_valid(repo, registered_address, current_address, registrar):
    new_patient = registrar.register_new_patient(
        national_id=NationalID(id='1234567890123'),
        first_name=Name(value='นนทพัฒน์'),
        last_name=Name(value='คนสุขภาพดี'),
        phone_number=PhoneNumber(value='0123456789'),
        date_of_birth=DateOfBirth(year=1990, month=12, day=31),
        registered_address=registered_address,
        current_address=current_address,
        rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY)
    )

    assert new_patient.national_id == NationalID(id='1234567890123')
    assert new_patient.rights.rights_type == PatientRights.SOCIAL_SECURITY
    saved_patient = repo.get_by_national_id(NationalID(id='1234567890123'))
    assert saved_patient is not None
    assert new_patient.id == saved_patient.id
    assert saved_patient.national_id == NationalID(id='1234567890123')
    assert saved_patient.version.number == 1


def test_registrar_patient_should_raise_error_when_duplicate_national_id(registrar, registered_address,
                                                                         current_address):
    common_id = NationalID(id='1234567890123')
    registrar.register_new_patient(
        national_id=common_id,
        first_name=Name(value='นนทพัฒน์'),
        last_name=Name(value='คนสุขภาพดี'),
        phone_number=PhoneNumber(value='0123456789'),
        date_of_birth=DateOfBirth(year=1990, month=12, day=31),
        registered_address=registered_address,
        current_address=current_address,
        rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY)
    )
    with raises(DuplicateNationalIDError) as error:
        registrar.register_new_patient(
            national_id=common_id,
            first_name=Name(value='นนทพัฒน์'),
            last_name=Name(value='คนสุขภาพดี'),
            phone_number=PhoneNumber(value='0123456789'),
            date_of_birth=DateOfBirth(year=1990, month=12, day=31),
            registered_address=registered_address,
            current_address=current_address,
            rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY)
        )
    assert 'เลขบัตรประชาชนนี้มีในระบบแล้ว' in str(error.value)


def test_patient_registrar_should_raise_error_when_national_id_invalid(registrar, registered_address, current_address):
    with raises(ValidationError) as error:
        registrar.register_new_patient(
            national_id=NationalID(id='132456'),
            first_name=Name(value='นนทพัฒน์'),
            last_name=Name(value='คนสุขภาพดี'),
            phone_number=PhoneNumber(value='0123456789'),
            date_of_birth=DateOfBirth(year=1990, month=12, day=31),
            registered_address=registered_address,
            current_address=current_address,
            rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY)
        )
    assert '132456' in str(error.value)


def test_patient_registrar_should_handle_repository_failure(registered_address, current_address):
    broken_repo = BrokenPatientRecord()
    unlucky_registrar = PatientRegistrar(repo=broken_repo)

    with raises(RuntimeError) as excinfo:
        unlucky_registrar.register_new_patient(
            national_id=NationalID(id='1100110011001'),
            first_name=Name(value='สมชาย'),
            last_name=Name(value='โชคร้าย'),
            phone_number=PhoneNumber(value='0811111111'),
            date_of_birth=DateOfBirth(year=1980, month=1, day=1),
            registered_address=registered_address,
            current_address=current_address,
            rights=Rights(rights_type=PatientRights.GOLD_CARD)
        )

    assert "Database พัง save ไม่ได้" in str(excinfo.value)


def test_patient_registrar_should_update_patient_info_through_repository(registered_address, current_address, registrar, repo):
    new_patient = registrar.register_new_patient(
        national_id=NationalID(id='1234567890123'),
        first_name=Name(value='นนทพัฒน์'),
        last_name=Name(value='คนสุขภาพดี'),
        phone_number=PhoneNumber(value='0123456789'),
        date_of_birth=DateOfBirth(year=1990, month=12, day=31),
        registered_address=registered_address,
        current_address=current_address,
        rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY)
    )
    new_phone = PhoneNumber(value='099-999-9999')
    new_patient.update_phone_number(new_phone)

    registrar.update_patient_info(new_patient)

    updated_in_repo = repo.get_by_national_id(new_patient.national_id)
    assert updated_in_repo.phone_number == new_phone
    assert updated_in_repo.version.number == 2

def test_patient_registrar_should_increment_version_when_update_patient_info(
        registered_address, current_address, registrar, repo
):
    new_patient = registrar.register_new_patient(
        national_id=NationalID(id='1234567890123'),
        first_name=Name(value='นนทพัฒน์'),
        last_name=Name(value='คนสุขภาพดี'),
        phone_number=PhoneNumber(value='0123456789'),
        date_of_birth=DateOfBirth(year=1990, month=12, day=31),
        registered_address=registered_address,
        current_address=current_address,
        rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY)
    )
    new_phone = PhoneNumber(value='099-999-9999')
    new_patient.update_phone_number(new_phone)
    registrar.update_patient_info(new_patient)
    updated_in_repo = repo.get_by_national_id(new_patient.national_id)
    assert updated_in_repo.phone_number == new_phone
    assert updated_in_repo.version.number == 2

    new_right = Rights(rights_type=PatientRights.COMPANY_INSURANCE)
    new_patient.update_rights(new_right)
    registrar.update_patient_info(new_patient)
    updated_in_repo = repo.get_by_national_id(new_patient.national_id)
    assert updated_in_repo.rights == new_right
    assert updated_in_repo.version.number == 3