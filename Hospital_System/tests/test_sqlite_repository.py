import os

from pandas.core import sample

from Hospital_System.domain.value_object import QueueStatus, Version, Diagnosis, MedicineInfo
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

    retrieved = repo.get_by_queue_id(pa_queue.id)
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
    updated_queue = repo.get_by_queue_id(sample_queue.id)

    assert updated_queue.status == QueueStatus.IN_PROGRESS
    assert updated_queue.version.number == 2

    queue_all = repo.get_all()
    assert len(queue_all) == 1
    os.remove(repo.db_path)


def test_sqlite_repo_should_return_none_when_queue_not_found(repo):
    repo.create_schema()
    import uuid
    random_id = uuid.uuid4()
    result_queue = repo.get_by_queue_id(random_id)
    assert result_queue is None
    os.remove(repo.db_path)


def test_sqlite_repo_should_return_empty_list_when_db_is_empty(repo):
    repo.create_schema()

    result = repo.get_all()
    assert isinstance(result, list)
    assert len(result) == 0
    os.remove(repo.db_path)

def test_sqlite_repo_should_save_extremely_long_diagnosis(repo, queue):
    repo.create_schema()
    queue.start_consultation()
    max_disease = 'ปวดหั' * 5
    max_treatment = 'ตัวร้อ' * 5
    queue.complete_visit(Diagnosis(
        disease=max_disease,
        treatment=max_treatment,
        medicine_prescribed=[MedicineInfo(
            name='Paracetamol',
            strength='500mg',
            frequency='วันละ 3 ครั้ง หลังอาหาร')]
        )
    )
    repo.save(queue)
    retrieved = repo.get_by_queue_id(queue.id)

    assert retrieved.id == queue.id
    assert retrieved.patient_id == queue.patient_id
    assert retrieved.status == QueueStatus.COMPLETED
    assert retrieved.diagnosis.disease == max_disease
    assert retrieved.diagnosis.treatment == max_treatment
    os.remove(repo.db_path)