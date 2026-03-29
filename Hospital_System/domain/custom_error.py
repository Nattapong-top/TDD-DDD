from pydantic import BaseModel
class DomainError(Exception):
    pass

class DuplicationQueueError(DomainError):
    pass