from Hospital_System.domain.interfaces import StaffRepository
from Hospital_System.domain.staff_entities import Staff
from Hospital_System.domain.value_object import Username
from Hospital_System.domain.custom_error import DuplicateUsernameError


class StaffService:
    def __init__(self, staff_repo: StaffRepository) -> None:
        self.staff_repo = staff_repo

    def register_staff(self,
                       username_str, password_str, national_id_str,
                       first_name_str, last_name_str, dob_year,
                       dob_month, dob_day, phone_number_str, role) -> Staff:

        self._chack_duplicate_username(username_str)

        new_staff = Staff.register(
            username_str=username_str,
            password_str=password_str,  # ส่งรหัสสดเข้าไป
            national_id_str=national_id_str,
            first_name_str=first_name_str,
            last_name_str=last_name_str,
            dob_year=dob_year, dob_month=dob_month, dob_day=dob_day,
            phone_number_str=phone_number_str,
            role=role
        )

        self.staff_repo.save(new_staff)
        return new_staff

    def _chack_duplicate_username(self, username_str):
        if self.staff_repo and self.staff_repo.get_by_username(Username(id=username_str)):
            raise DuplicateUsernameError(f'ชื่อ {username_str} มีคนใช้แล้ว')
