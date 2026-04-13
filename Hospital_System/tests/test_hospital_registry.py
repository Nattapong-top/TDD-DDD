# tests/test_hospital_registry.py
import os

from pytest import fixture, raises
from Hospital_System.domain.hospital_registry import QueueRegistry
from Hospital_System.domain.domain_service.queue_service import QueueService
from Hospital_System.domain.custom_error import RegistryNotConfiguredError
from Hospital_System.infrastructure.sqlite_queue_repository import SqlQueueRepository
from Hospital_System.tests.test_domain_service import FakeQueueRecord


@fixture
def fake_repo():
    return FakeQueueRecord()


def test_hospital_registry_should_return_queue_service_after_configuration(fake_repo):
    QueueRegistry.configure(queue_repo=fake_repo)
    assert isinstance(QueueRegistry.queue_service(), QueueService)

def test_hospital_registry_should_raise_error_when_access_before_configure():
    QueueRegistry._queue_service = None
    with raises(RegistryNotConfiguredError) as err:
        QueueRegistry.queue_service()

    assert 'Queue Service ยังไม่ได้ Configure' in str(err.value)



@fixture
def sql_repo():
    return SqlQueueRepository(db_path='test.db')

def test_hospital_registry_should_configure_with_real_sqlite_repository(sql_repo):
    sql_repo.create_schema()
    QueueRegistry.configure(queue_repo=sql_repo)
    service = QueueRegistry.queue_service()
    assert isinstance(service, QueueService)
    assert isinstance(service.repo, SqlQueueRepository)

    assert isinstance(QueueRegistry.queue_service(), QueueService)
    os.remove('test.db')
