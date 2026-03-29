from abc import ABC, abstractmethod
from typing import Optional

from Hospital_System.domain.entities import Queue


class QueueRecord(ABC):
    @abstractmethod
    def get_last_queue(self) -> Optional[Queue]:
        pass

    @abstractmethod
    def save(self, queue: Queue) -> None:
        pass