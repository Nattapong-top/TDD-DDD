import os

from pandas.core import sample

from Hospital_System.domain.value_object import QueueStatus, Version
from Hospital_System.infrastructure.persistence.sqlite_repository import SqlQueueRepository
from Hospital_System.tests.test_entity import patient, queue
from pytest import fixture


@fixture
def repo():
    db_path = 'test_hospital.db'
    if os.path.exists(db_path): os.remove(db_path)
    return SqlQueueRepository(db_path=db_path)


def test_sqlite_repo_should_save_and_retrieve_queue(patient, queue, repo):
    repo.create_schema()
    pa_queue = queue
    repo.save(pa_queue)

    retrieved = repo.get_by_id(pa_queue.id)
    assert retrieved.id == pa_queue.id
    assert retrieved.patient_id == pa_queue.patient_id
    assert retrieved.vital_signs.blood_pressure.systolic == 120
    assert retrieved.vital_signs.temperature.value == 39.0
    assert retrieved.vital_signs.symptom == 'น้ำหมูกไหล ปวดหัว ตัวร้อน หนาวสั่น'

    os.remove(repo.db_path)

def test_sqlite_repo_should_update_existing_queue(patient, queue, repo):
    repo.create_schema()
    sample_queue = queue
    assert sample_queue.status == QueueStatus.WAITING

    repo.save(sample_queue)
    sample_queue.start_consultation()
    repo.save(sample_queue)
    updated_queue = repo.get_by_id(sample_queue.id)

    assert updated_queue.status == QueueStatus.IN_PROGRESS
    assert updated_queue.version.number == 2

    queue_all = repo.get_all()
    assert len(queue_all) == 1
