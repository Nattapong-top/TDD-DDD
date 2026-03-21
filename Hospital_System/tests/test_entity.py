import uuid

from _pytest.fixtures import fixture

from Hospital_System.domain.value_object import (
    Name, PhoneNumber, DateOfBirth, Address, Province, PatientRights, NationalID, Rights)

from Hospital_System.domain.entities import Patient

@fixture
def patient():
    return Patient(
        id=uuid.uuid4(),
        nation_id=NationalID(id='1234567890123'),
        first_name = Name(value='นนทพัฒน์'),
        last_name = Name(value='คนสุขภาพดี'),
        phone_number = PhoneNumber(value='0123456789'),
        date_of_birth = DateOfBirth(year=1990, month=12, day=31),
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
        right=Rights(rights_type=PatientRights.SOCIAL_SECURITY)
    )

def test_create_patient_is_validate(patient):

    assert patient.id is not None
    assert patient.nation_id.id == '1234567890123'
    assert patient.first_name.value == 'นนทพัฒน์'
    assert patient.phone_number == PhoneNumber(value='0123456789')
    assert patient.right == Rights(rights_type=PatientRights.SOCIAL_SECURITY)