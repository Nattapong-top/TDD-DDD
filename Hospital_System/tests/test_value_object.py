# Unit Tests for Hospital_System
from pydantic import ValidationError
from pytest import raises, fixture, approx

from Hospital_System.domain.value_object import Name


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