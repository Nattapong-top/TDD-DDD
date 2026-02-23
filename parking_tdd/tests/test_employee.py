import pytest
from domain.models import Employee
from domain.value_object import FirstName, LastName


def test_create_employee_profile():
    fname = FirstName(value='ณัฐพงศ์')
    lname = LastName(value='คนเก่ง')

    assert fname.value == 'ณัฐพงศ์'
    assert lname.value == 'คนเก่ง'


def test_create_employee_empty_profile():
    with pytest.raises(ValueError):
        FirstName(value='    ')
    with pytest.raises(ValueError):
        LastName(value='       ')


def test_first_name_too_short():
    with pytest.raises(ValueError):
        FirstName(value='ก')
    with pytest.raises(ValueError):
        LastName(value='ง')


def test_employee_entiry_should_have_id_and_full_name():
    fname = FirstName(value='ณัฐพงศ์')
    lname = LastName(value='ป๋าไอที')
    emp = Employee(emp_id=101, first_name=fname, last_name=lname)

    assert emp.emp_id == 101
    assert emp.get_full_name() == 'ณัฐพงศ์ ป๋าไอที'


def test_employee_change_last_name_to_same_one_should_fail():
    fname = FirstName(value='ณัฐพงศ์')
    lname = LastName(value='ป๋าไอที')
    emp = Employee(emp_id=101, first_name=fname, last_name=lname)

    # ลองเปลี่ยนเป็นนามสกุลเดิม ("ป๋าไอที")
    with pytest.raises(ValueError):
        new_lname = LastName(value='ป๋าไอที')
        emp.change_last_name(new_lname=new_lname)