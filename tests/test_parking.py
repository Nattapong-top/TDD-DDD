import pytest
from domain.models import Employee
from domain.value_object import ParkingHour, FirstName, LastName


def test_parking_hour_should_fail_if_negetive():
    # โจทย์: ถ้าส่ง -1 เข้าไป ต้องระเบิด (ValueError)
    with pytest.raises(ValueError):
        ParkingHour(value=-1)

def test_parking_hour_should_fail_if_24():
    with pytest.raises(ValueError):
        ParkingHour(value=25)

def test_parking_hour_normal_5():
    hour = ParkingHour(value=5)
    assert hour.value == 5

def test_parking_hour_rounding_up():
    # โจทย์: ถ้าจอด 5.1 ชม. ป๋าต้องปัดเป็น 6 ชม. (ปัดขึ้นเสมอ)
    hour = ParkingHour(value=5.1)
    assert hour.value == 6

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