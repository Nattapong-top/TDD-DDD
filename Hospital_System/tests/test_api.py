# Hospital_System/tests/test_api.py


def test_api_register_new_patient_should_return_success(client):
    # 1. จำลองข้อมูล JSON ที่หน้าเว็บจะส่งมาให้ (เหมือนกรอกฟอร์ม)
    payload = {
        "national_id": "1999999999999",
        "first_name": "สมชาย",
        "last_name": "ใจดี",
        "phone_number": "0812345678",
        "dob_year": 1990, "dob_month": 1, "dob_day": 1,
        "house_number": "99/9", "street": "สุขุมวิท",
        "sub_district": "คลองเตย", "district": "คลองเตย",
        "province": "กรุงเทพมหานคร", "postal_code": "10110",
        "rights_type": "ประกันสังคม",
        "systolic": 120, "diastolic": 80,
        "weight": 70.0, "height": 175.0, "temperature": 36.5,
        "symptom": "ปวดหัว ตัวร้อน"
    }

    # 2. ยิง API แบบ POST ไปที่ประตูรับลงทะเบียน
    response = client.post('/api/patients/register', json=payload)

    # 3. ตรวจข้อสอบ
    assert response.status_code == 200  # ต้องตอบกลับว่าสำเร็จ (200 OK)
    data = response.json()
    assert 'queue_id' in data # ต้องมีรหัสคิวส่งกลับมา
    assert 'queue_number' in data
    assert data['status'] == 'รอ' # สถานะคิวต้องเป็น "รอ"