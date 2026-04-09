#tests.test_patient_registrar
from pytest import fixture, raises

from Hospital_System.domain.domain_service.patient_registrar import PatientRegistrar
from Hospital_System.domain.entities import Patient
from Hospital_System.domain.value_object import Address, Province, NationalID, Name, PhoneNumber, DateOfBirth, Rights, \
    PatientRights
from Hospital_System.domain.custom_error import DuplicateNationalIDError

class FakePatientRecord:
    def __init__(self) -> None:
        self.patients = {}

    def save(self, patient: Patient) -> None:
        self.patients[patient.id] = patient

    def get_by_nation_id(self, nation_id: str) -> Patient | None:
        return next((p for p in self.patients.values() if p.nation_id.id == nation_id), None)


@fixture
def repo() -> FakePatientRecord:
    return FakePatientRecord()

@fixture
def registrar(repo) -> PatientRegistrar:
    return PatientRegistrar(repo=repo)


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
            nation_id=NationalID(id='1234567890123'),
            first_name=Name(value='นนทพัฒน์'),
            last_name=Name(value='คนสุขภาพดี'),
            phone_number=PhoneNumber(value='0123456789'),
            date_of_birth=DateOfBirth(year=1990, month=12, day=31),
            registered_address=registered_address,
            current_address=current_address,
            rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY)
        )

        assert new_patient.nation_id == NationalID(id='1234567890123')
        assert new_patient.rights.rights_type == PatientRights.SOCIAL_SECURITY
        saved_patient = repo.get_by_nation_id('1234567890123')
        assert saved_patient is not None
        assert new_patient.id == saved_patient.id
        assert saved_patient.nation_id == NationalID(id='1234567890123')


def test_registrar_patient_should_raise_error_when_duplicate_nation_id(registrar, registered_address, current_address):
    common_id = NationalID(id='1234567890123')
    registrar.register_new_patient(
        nation_id=common_id,
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
            nation_id=common_id,
            first_name=Name(value='นนทพัฒน์'),
            last_name=Name(value='คนสุขภาพดี'),
            phone_number=PhoneNumber(value='0123456789'),
            date_of_birth=DateOfBirth(year=1990, month=12, day=31),
            registered_address=registered_address,
            current_address=current_address,
            rights=Rights(rights_type=PatientRights.SOCIAL_SECURITY)
        )
    assert 'เลขบัตรประชาชนนี้มีในระบบแล้ว' in str(error.value)