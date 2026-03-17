# Unit Tests for Hospital_System
from pydantic import ValidationError
from pytest import raises, fixture, approx

from Hospital_System.domain.value_object import Name, PhoneNumber


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

def test_should_create_PhoneNuber_is_Hyphen_and_number():
    phone = PhoneNumber(value='012-345-6789')
    assert phone.value == '0123456789'

def test_should_raise_PhoneNumber_start_Not_zero():
    with raises(ValueError):
        PhoneNumber(value='9123456789')
