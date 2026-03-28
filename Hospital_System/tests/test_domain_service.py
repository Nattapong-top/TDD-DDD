# test_domain_service.py
from pytest import fixture
from datetime import date, datetime
from Hospital_System.domain.domain_service import QueueService
from Hospital_System.domain.value_object import Number

@fixture
def today_date() -> date:
    return date(2026, 3, 28)

@fixture
def now() -> datetime:
    return datetime(2026, 3, 28,
                    22, 43, 53, 302903)

def test_should_queue_service_issue_first_number_of_the_day():
    service = QueueService()

    today = date(2026, 3, 28)
    now = datetime(2026, 3, 28, 22, 43, 53, 302903)
    next_number, last_date, time_now = service.get_next_number(
        last_number=Number(id=0), last_date=today, time_now=now, today=today)
    assert next_number == Number(id=1)
    assert last_date == date(2026, 3, 28)
    assert time_now == datetime(2026, 3, 28, 22, 43, 53, 302903)

def test_should_queue_service_reset_number_and_last_date(today_date, now):
    service = QueueService()
    next_number, last_date, time_now = service.get_next_number(
        last_number=Number(id=99), last_date=date(2026, 3, 27),
        time_now=now, today=today_date)
    assert next_number == Number(id=1)
    assert last_date == date.today()
    assert time_now == now
