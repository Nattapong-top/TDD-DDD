from Hospital_System.domain.staff_entities import Staff


class StaffService:
    def __init__(self, staff_repo=None) -> None:
        self.staff_repo = staff_repo

    def register_staff(self,
                       username_str, password_str, national_id_str,
                       first_name_str, last_name_str, dob_year,
                       dob_month, dob_day, phone_number_str, role) -> Staff:

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

        return new_staff
