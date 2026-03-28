# test_domain_service.py
import datetime
import time

import pytest
from datetime import date, datetime
from Hospital_System.domain.domain_service import QueueService
from Hospital_System.domain.value_object import Number


def test_should_queue_service_issue_first_number_of_the_day():
    service = QueueService()

    today = date(2026, 3, 28)
    now = datetime(2026, 3, 28, 22, 43, 53, 302903)
    next_number, current_date, time_now = service.get_next_number(
        last_number=Number(id=0), current_date=today, time_now=now)
    assert next_number == Number(id=1)
    assert current_date == date(2026, 3, 28)
    assert time_now == datetime(2026, 3, 28, 22, 43, 53, 302903)

