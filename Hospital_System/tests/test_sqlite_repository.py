import os

from Hospital_System.infrastructure.persistence.sqlite_repository import SqlQueueRepository
from Hospital_System.tests.test_entity import patient, queue


def test_sqlite_repo_should_save_and_retrieve_queue(patient, queue):
    db_path = r'test_hospital.db'
    if os.path.exists(db_path): os.remove(db_path)

    repo = SqlQueueRepository(db_path=db_path)
    repo.create_schema()

    pa_queue = queue
    repo.save(pa_queue)

    retrieved = repo.get_by_id(pa_queue.id)
    assert retrieved.id == pa_queue.id
    assert retrieved.patient_id == pa_queue.patient_id
    assert retrieved.vital_signs.blood_pressure.systolic == 120
    assert retrieved.vital_signs.temperature.value == 39.0
    assert retrieved.vital_signs.symptom == 'น้ำหมูกไหล ปวดหัว ตัวร้อน หนาวสั่น'

    os.remove(db_path)


