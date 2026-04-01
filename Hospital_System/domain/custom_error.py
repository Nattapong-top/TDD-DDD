from pydantic import BaseModel
class DomainError(Exception):
    pass

class DuplicationQueueError(DomainError):
    pass

class InvalidStatusTransitionError(DomainError):
    pass

class MissingDiagnosisError(DomainError):
    pass