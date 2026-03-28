# domain_service.py
from typing import Tuple

from datetime import datetime, date

from Hospital_System.domain.value_object import Number


class QueueService:
    def get_next_number(self, last_number:Number, last_date: date, time_now: datetime, today: date) -> Tuple[Number,date, datetime]:
        last_number, last_date = self._reset_date_and_number(last_number, last_date, today)
        now_number = Number(id=last_number.id + 1)
        return now_number, last_date, time_now

    def _reset_date_and_number(self, last_number: Number, last_date: date, today: date) -> tuple[Number, date]:
        if last_date < today:
            last_date = today
            last_number = Number(id=0)
        return last_number, last_date