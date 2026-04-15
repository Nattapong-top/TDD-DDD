from Hospital_System.domain.value_object import QueueStatus


def test_register_new_patient_should_auto_create_queue(
        queue_service, new_patient):
    active_queue = queue_service.get_active_queue_by_patient(new_patient.id)
    assert active_queue is not None
    assert active_queue.patient_id == new_patient.id
    assert active_queue.status == QueueStatus.WAITING