from uuid import UUID

from Hospital_System.domain.domain_service.staff_service import StaffService
from Hospital_System.domain.value_object import StaffRole, HashedPassword, DateOfBirth


def test_staff_service_register_new_staff_should_succeed():
    new_staff = StaffService().register_staff(
        username_str="nattapong-top",
        password_str="Paa-TopIT_12123",  # ส่งรหัสสดเข้าไป
        national_id_str="1234567890123",
        first_name_str="ณัฐพงศ์",
        last_name_str="คนรักษาดี",
        dob_year=1990, dob_month=12, dob_day=31,
        phone_number_str="0999999999",
        role=StaffRole.DOCTOR
    )
    assert new_staff.username.id == "nattapong-top"
    assert new_staff.national_id.id == '1234567890123'
    assert isinstance(new_staff.hashed_password, HashedPassword)
    assert new_staff.hashed_password.value != "Paa-TopIT_12123"
    assert new_staff.role == StaffRole.DOCTOR

def test_staff_service_register_staff_with_staff_id_should_type_uuid_valid(new_register_staff):
    staff_1 = new_register_staff
    staff_2 = StaffService().register_staff(
        username_str="nattapong-top",
        password_str="Paa-TopIT_12123",  # ส่งรหัสสดเข้าไป
        national_id_str="1234567890123",
        first_name_str="ณัฐพงศ์",
        last_name_str="คนรักษาดี",
        dob_year=1990, dob_month=12, dob_day=31,
        phone_number_str="0999999999",
        role=StaffRole.DOCTOR
    )

    assert staff_1.staff_id is not None
    assert staff_2.staff_id is not None
    assert isinstance(staff_1.staff_id, UUID)
    assert staff_1.staff_id != staff_2.staff_id
    print('\n',staff_1.staff_id)
    print(staff_2.staff_id)
