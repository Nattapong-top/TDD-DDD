# tests/test_registry.py
from pytest import fixture, raises
from Hospital_System.domain.registry import DomainRegistry
from Hospital_System.domain.domain_service import QueueService
from Hospital_System.domain.custom_error import RegistryNotConfiguredError
from Hospital_System.tests.test_domain_service import FakeQueueRecord


@fixture
def repo():
    return FakeQueueRecord()


def test_registry_should_return_queue_service_after_configuration(repo):
    DomainRegistry.configure(queue_repo=repo)
    assert isinstance(DomainRegistry.queue_service(), QueueService)

def test_registry_should_raise_error_when_access_before_configure():
    DomainRegistry._queue_service = None
    with raises(RegistryNotConfiguredError) as err:
        DomainRegistry.queue_service()

    assert 'Queue Service ยังไม่ได้ Configure' in str(err.value)

