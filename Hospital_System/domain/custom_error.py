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


class VitalSignsMissingError(DomainError):
    """ด่าเวลาพยายามออกคิวโดยไม่มีสัญญาณชีพ"""

    def __init__(self, message="ป๋าครับ! ไม่มีสัญญาณชีพ ออกคิวให้ไม่ได้นะ!"):
        self.message = message
        super().__init__(self.message)

class QueueNotFoundError(DomainError):
    def __init__(self, queue_id=None):
        if queue_id:
            self.message = f'ไม่พบคิว ID: {queue_id} นี้ในระบบครับ'
        else:
            self.message = 'ไม่พบคิวที่ระบุครับ'
        super().__init__(self.message)