# tests/test_registry.py
import os

from pytest import fixture, raises
from Hospital_System.domain.registry import DomainRegistry
from Hospital_System.domain.domain_service import QueueService
from Hospital_System.domain.custom_error import RegistryNotConfiguredError
from Hospital_System.infrastructure.persistence.sqlite_repository import SqlQueueRepository
from Hospital_System.tests.test_domain_service import FakeQueueRecord


@fixture
def fake_repo():
    return FakeQueueRecord()


def test_registry_should_return_queue_service_after_configuration(fake_repo):
    DomainRegistry.configure(queue_repo=fake_repo)
    assert isinstance(DomainRegistry.queue_service(), QueueService)

def test_registry_should_raise_error_when_access_before_configure():
    DomainRegistry._queue_service = None
    with raises(RegistryNotConfiguredError) as err:
        DomainRegistry.queue_service()

    assert 'Queue Service ยังไม่ได้ Configure' in str(err.value)



@fixture
def sql_repo():
    return SqlQueueRepository(db_path='test.db')

def test_registry_should_configure_with_real_sqlite_repository(sql_repo):
    sql_repo.create_schema()
    DomainRegistry.configure(queue_repo=sql_repo)
    service = DomainRegistry.queue_service()
    assert isinstance(service, QueueService)
    assert isinstance(service.repo, SqlQueueRepository)

    assert isinstance(DomainRegistry.queue_service(), QueueService)
    os.remove('test.db')
