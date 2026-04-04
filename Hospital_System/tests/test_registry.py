# tests/test_registry.py
from pytest import fixture
from Hospital_System.domain.registry import DomainRegistry
from Hospital_System.domain.domain_service import QueueService
from Hospital_System.tests.test_domain_service import FakeQueueRecord


@fixture
def repo():
    return FakeQueueRecord()


def test_registry_should_return_queue_service_after_configuration(repo):
    DomainRegistry.configure(queue_repo=repo)
    assert isinstance(DomainRegistry.queue_service(), QueueService)
