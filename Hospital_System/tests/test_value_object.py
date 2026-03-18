# Unit Tests for Hospital_System
from pydantic import ValidationError
from pytest import raises, fixture, approx
from datetime import date
from Hospital_System.domain.value_object import Name, PhoneNumber, DateOfBirth


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