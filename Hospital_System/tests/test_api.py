# Hospital_System/tests/test_api.py


def test_api_register_new_patient_should_return_success(client, valid_patient_payload):
    # 1. จำลองข้อมูล JSON ที่หน้าเว็บจะส่งมาให้ (เหมือนกรอกฟอร์ม)

    # 2. ยิง API แบบ POST ไปที่ประตูรับลงทะเบียน
    response = client.post('/api/patients/register', json=valid_patient_payload)

    # 3. ตรวจข้อสอบ
    assert response.status_code == 200  # ต้องตอบกลับว่าสำเร็จ (200 OK)
    data = response.json()
    assert data['national_id'] == valid_patient_payload['national_id']
    assert data['first_name'] == valid_patient_payload['first_name']



def test_api_registrar_patient_duplicate_should_return_same_id(client, valid_patient_payload):
    # ยิงครั้งแรก (สร้างใหม่)
    res1 = client.post('/api/patients/register', json=valid_patient_payload)
    id1 = res1.json()['national_id']

    # ยิงครั้งที่ 2 (ข้อมูลเดิม)
    res2 = client.post('/api/patients/register', json=valid_patient_payload)
    id2 = res2.json()['national_id']

    # ตรวจสอบ: ต้อง 200 OK และ ID ตรงกัน
    assert res1.status_code == 200
    assert res2.status_code == 200
    assert id1 == id2
    assert res2.json()['message'] == 'ลงทะเบียนสำเร็จ!'

def test_api_registrar_patient_should_fail_when_invalid_nation_id(client, valid_patient_payload):
    bad_payload = valid_patient_payload.copy()
    bad_payload['national_id'] = 'XYZ-888888888'

    response = client.post('/api/patients/register', json=bad_payload)

    assert response.status_code == 400
    assert 'String should match pattern' in response.json()['detail']