# Unit Tests for Hospital_System
from pydantic import ValidationError
from pytest import raises, fixture, approx
from datetime import date
from Hospital_System.domain.value_object import (
    Name, PhoneNumber, DateOfBirth, Address, Province, PatientRights, Rights, BloodPressure, Weight, Height)


# ส่วนของ VO Name เทสชื่อและนามสกุล
def test_should_create_Name_is_valid():
    first_name = Name(value='นนทพัฒน์')
    last_name = Name(value='คนสุขภาพดี')

    assert first_name.value == 'นนทพัฒน์'
    assert last_name.value == 'คนสุขภาพดี'

def test_should_raise_error_Name_is_too_long():
    with raises(ValueError):
        Name(value='นนทพัฒน์'*20)

def test_should_raise_error_Name_is_emtpy():
    with raises(ValueError):
        Name(value='')

def test_should_raise_error_Name_is_number():
    with raises(ValueError):
        Name(value='123456789')

def test_should_raise_error_Name_is_whitespace():
    with raises(ValueError):
        Name(value='       ')

def test_should_raise_error_Name_is_str_and_number():
    with raises(ValueError):
        Name(value='ชื่อภาษาไทยบวกตัวเลข1')

# ส่วนของ VO PhoneNumber เทสเบอร์โทรศัพท์
def test_should_create_PhoneNumber_is_valid():
    phone = PhoneNumber(value='0123456789')
    assert phone.value == '0123456789'

def test_should_raise_error_PhoneNumber_is_too_long():
    with raises(ValueError):
        PhoneNumber(value='05456123456789')

def test_should_raise_error_PhoneNumber_is_emtpy():
    with raises(ValueError):
        PhoneNumber(value='')

def test_should_raise_error_PhoneNumber_is_whitespace():
    with raises(ValueError):
        PhoneNumber(value='   ')

def test_should_raise_error_PhoneNumber_is_str_and_number():
    with raises(ValueError):
        PhoneNumber(value='0234567dfg')

def test_should_create_PhoneNumber_is_Hyphen_and_number():
    phone = PhoneNumber(value='012-345-6789')
    assert phone.value == '0123456789'

def test_should_raise_PhoneNumber_start_Not_zero():
    with raises(ValueError):
        PhoneNumber(value='9123456789')

# ส่วนของ VO Age เทสอายุ
def test_should_create_DateOfBirth_is_valid():
    dob = DateOfBirth(year=1990, month=12, day=31)
    assert dob.year == 1990
    assert dob.month == 12
    assert dob.day == 31

def test_should_raise_error_DateOfBirth_month_out_of_range():
    with raises(ValueError):
        DateOfBirth(year=1990, month=13, day=31)

def test_should_raise_error_DateOfBirth_day_out_of_range():
    with raises(ValueError):
        DateOfBirth(year=1990, month=12, day=32)

def test_should_raise_error_DateOfBirth_is_future_dae():
    with raises(ValueError):
        DateOfBirth(year=2026, month=12, day=31)

def test_should_raise_error_DateOfBirth_is_Over_150_years():
    today = date.today()
    with raises(ValueError):
        DateOfBirth(year=today.year - 151, month=12, day=31)

def test_should_create_DateOfBirth_is_today():
    today = date.today()
    dob = DateOfBirth(year=today.year, month=today.month, day=today.day)
    assert dob.year == today.year
    assert dob.month == today.month
    assert dob.day == today.day

# ส่วนของ VO Address เทสที่อยู่
def test_should_create_registered_Address_is_valid():
    registered_address = Address(
        house_number='10',
        street='วิวิธสุรการ',
        sub_district='มุกดาหาร',
        district='เมือง',
        province=Province.MUKDAHAN,
        postal_code='49000'
    )  # เลขที่ 10 ถนนวิวิธสุรการ ต.มุกดาหาร อ.เมือง จ.มุกดาหาร 49000

    assert registered_address.house_number == '10'
    assert registered_address.street == 'วิวิธสุรการ'
    assert registered_address.sub_district == 'มุกดาหาร'
    assert registered_address.district == 'เมือง'
    assert registered_address.province == Province.MUKDAHAN
    assert registered_address.postal_code == '49000'

def test_should_create_current_Address_is_valid():
    current_address = Address(  # ตั้งอยู่ที่ 173 ถนนดินสอ แขวงเสาชิงช้า เขตพระนคร กรุงเทพมหานคร 10200
        house_number='173',
        street='ดินสอ',
        sub_district='เสาชิงช้า',
        district='พระนคร',
        province=Province.BANGKOK,
        postal_code='10200'
    )
    assert current_address.house_number == '173'
    assert current_address.street == 'ดินสอ'
    assert current_address.sub_district == 'เสาชิงช้า'
    assert current_address.district == 'พระนคร'
    assert current_address.province == Province.BANGKOK
    assert current_address.postal_code == '10200'

def test_should_raise_error_when_province_is_invalid_NotInEnum():
    with raises(ValueError):
        Address(
            house_number='10',
            street='วิวิธสุรการ',
            sub_district='มุกดาหาร',
            district='เมือง',
            province='มุกดา',
            postal_code='49000'
        )

def test_should_raise_error_when_postal_code_is_invalid_str_over_5():
    with raises(ValueError):
        registered_address = Address(
            house_number='10',
            street='วิวิธสุรการ',
            sub_district='มุกดาหาร',
            district='เมือง',
            province=Province.MUKDAHAN,
            postal_code='49000dfg'
        )
def test_should_create_Address_when_without_street_is_valid():
    address = Address(
        house_number='10',
        street=None,
        sub_district='มกดาหาร',
        district='เมือง',
        province=Province.MUKDAHAN,
        postal_code='49000'
    )
    assert address.street is None

def test_should_create_PatientRights_is_valid():
    rights = PatientRights.GOLD_CARD
    assert rights == PatientRights.GOLD_CARD

def test_should_raise_error_when_PatientRights_is_invalid_NotInEnum():
    with raises(ValueError):
        PatientRights('บัตรหมดอายุ')

def test_should_create_Rights_is_valid():
    rights = Rights(rights_type=PatientRights.COMPANY_INSURANCE)
    assert rights.rights_type == PatientRights.COMPANY_INSURANCE

def test_should_raise_error_when_PatientRights_type_is_invalid_NotInEnum():
    with raises(ValueError):
        Rights(rights_type='บัตรดำ')

# ส่วนของ VO BloodPressure เทสวัดชีพจร
def test_should_create_BloodPressure_is_valid():
    blood_pressure = BloodPressure(systolic=120, diastolic=80)
    assert blood_pressure == BloodPressure(systolic=120, diastolic=80)

def test_should_raise_error_when_BloodPressure_systolic_over_of_range():
    with raises(ValueError):
        BloodPressure(systolic=200, diastolic=80)

def test_should_raise_error_when_BloodPressure_systolic_lower_of_range():
    with raises(ValueError):
        BloodPressure(systolic=120, diastolic=8)

def test_should_raise_error_when_BloodPressure_diastolic_over_range():
    with raises(ValueError):
        BloodPressure(systolic=120, diastolic=91)

def test_should_raise_error_when_BloodPressure_diastolic_lower_of_range():
    with raises(ValueError):
        BloodPressure(systolic=120, diastolic=9)

# ส่วนของ VO Weight เทสน้ำหนัก
def test_should_create_Weight_is_valid():
    weight = Weight(value=80)
    assert weight == Weight(value=80)

def test_should_raise_error_when_Weight_over_of_range():
    with raises(ValueError):
        Weight(value=301)

def test_should_raise_error_when_Weight_lower_of_range():
    with raises(ValueError):
        Weight(value=0.1)

def test_should_raise_error_when_Weight_input_str():
    with raises(ValueError):
        Weight(value='สิบ')

def test_should_raise_error_when_Weight_is_negative():
    with raises(ValueError):
        Weight(value=-1)

# ส่วนของ VO Height เทสส่วนสูง
def test_should_create_Height_is_valid():
    height = Height(value=80)
    assert height == Height(value=80)

def test_should_raise_error_when_Height_over_of_range():
    with raises(ValueError):
        Height(value=301)

def test_should_raise_error_when_Height_lower_of_range():
    with raises(ValueError):
        Height(value=0.1)

def test_should_raise_error_when_Height_input_str():
    with raises(ValueError):
        Height(value='สิบ')

def test_should_raise_error_when_Height_is_negative():
    with raises(ValueError):
        Height(value=-1)
