# tests/test_hospital_registry.py
import os
from pytest import fixture, raises

# --- โซนงานบริหาร (Domain Service): นำเข้าตัวพยาบาลและเจ้าหน้าที่ ---
from Hospital_System.domain.hospital_registry import HospitalRegistry
from Hospital_System.domain.domain_service.queue_service import QueueService
from Hospital_System.domain.domain_service.patient_registrar import PatientRegistrar
from Hospital_System.domain.custom_error import RegistryNotConfiguredError

# --- โซนงานช่าง (Infrastructure): นำเข้าตู้เก็บของจริง ---
from Hospital_System.infrastructure.sqlite_queue_repository import SqlQueueRepository
from Hospital_System.infrastructure.sqlite_patient_repository import SqlPatientRecord
from Hospital_System.tests.test_domain_service import FakeQueueRecord


# --- 1. Fixture สำหรับการจัดการไฟล์ DB ในการเทส ---
@fixture(autouse=True)
def clear_registry():
    """ล้างค่าใน Registry ทุกครั้งก่อนและหลังเทสแต่ละเคส เพื่อไม่ให้ค่าค้าง"""
    HospitalRegistry.reset()
    yield
    HospitalRegistry.reset()
    # ลบไฟล์ DB ที่อาจจะเกิดขึ้นจากการเทส (ถ้ามี)
    if os.path.exists('hospital_database.db'):
        os.remove('hospital_database.db')


@fixture
def fake_repo():
    return FakeQueueRecord()


@fixture
def sql_repo():
    return SqlQueueRepository(db_path='test.db')


def test_hospital_registry_should_return_queue_service_after_configuration(fake_repo):
    HospitalRegistry.configure(queue_repo=fake_repo)
    assert isinstance(HospitalRegistry.queue_service(), QueueService)


def test_hospital_registry_should_raise_error_when_access_before_configure():
    HospitalRegistry._queue_service = None
    with raises(RegistryNotConfiguredError) as err:
        HospitalRegistry.queue_service()

    assert 'Queue Service ยังไม่ได้ Configure' in str(err.value)


def test_hospital_registry_should_configure_with_real_sqlite_repository(sql_repo):
    sql_repo.create_schema()
    HospitalRegistry.configure(queue_repo=sql_repo)
    service = HospitalRegistry.queue_service()
    assert isinstance(service, QueueService)
    assert isinstance(service.repo, SqlQueueRepository)

    assert isinstance(HospitalRegistry.queue_service(), QueueService)
    os.remove('test.db')


def test_hospital_registry_should_get_patient_registrar_with_auto_wiring():
    """เทสว่า Registry สามารถประกอบร่างพยาบาลทะเบียนกับตู้ SQLite ให้เราได้เอง"""
    registrar = HospitalRegistry.patient_registrar()

    # ตรวจความถูกต้อง
    assert isinstance(registrar, PatientRegistrar)
    # ตรวจว่าพยาบาลถือตู้ SQLite จริงหรือเปล่า
    assert isinstance(registrar.repo, SqlPatientRecord)


def test_hospital_registry_should_return_same_when_call_patient_registrar_instance():
    """เทสว่าเรียกกี่ครั้งก็ได้พยาบาลคนเดิม (Singleton) ไม่สร้างใหม่ฟุ่มเฟือย"""
    first_call = HospitalRegistry.patient_registrar()
    second_call = HospitalRegistry.patient_registrar()

    assert first_call == second_call
