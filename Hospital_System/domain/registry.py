# domain/registry.py
from typing import Optional

from Hospital_System.domain.repository import QueueRecord
from Hospital_System.domain.domain_service import QueueService


class DomainRegistry():
    _queue_service: Optional[QueueService] = None

    @classmethod
    def configure(cls, queue_repo: QueueRecord) -> None:
        cls._queue_service = QueueService(repo=queue_repo)

    @classmethod
    def queue_service(cls) -> QueueService | None:
        return cls._queue_service
