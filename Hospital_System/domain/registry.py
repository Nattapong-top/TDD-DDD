# domain/registry.py
from typing import Optional

from Hospital_System.domain.repository import QueueRecord
from Hospital_System.domain.domain_service import QueueService
from Hospital_System.domain.custom_error import RegistryNotConfiguredError


class DomainRegistry():
    _queue_service: Optional[QueueService] = None

    @classmethod
    def configure(cls, queue_repo: QueueRecord) -> None:
        cls._queue_service = QueueService(repo=queue_repo)

    @classmethod
    def queue_service(cls) -> QueueService:
        cls._validation_none_type()
        return cls._queue_service

    @classmethod
    def _validation_none_type(cls):
        if cls._queue_service is None:
            raise RegistryNotConfiguredError('Queue Service ยังไม่ได้ Configure')
