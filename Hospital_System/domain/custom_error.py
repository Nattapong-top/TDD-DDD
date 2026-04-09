from pydantic import BaseModel


class DomainError(Exception):
    pass


class DuplicationQueueError(DomainError):
    pass


class InvalidStatusTransitionError(DomainError):
    pass


class MissingDiagnosisError(DomainError):
    pass


class InvalidCancelRequestError(DomainError):
    pass


class RegistryNotConfiguredError(DomainError):
    pass


class DuplicateNationalIDError(DomainError):
    pass
