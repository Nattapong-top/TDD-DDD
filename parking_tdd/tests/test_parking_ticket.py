import pytest
from domain.models import ParkingTicket

def test_parking_ticket_versioning():
    ticket1 = ParkingTicket(ticket_id=1)
    assert ticket1.version == 1
    ticket1.mark_as_paid()
    assert ticket1.ticket_id == 1
    assert ticket1.version == 2
    assert ticket1.is_paid == True
