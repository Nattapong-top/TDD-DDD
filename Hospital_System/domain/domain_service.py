# domain_service.py
from typing import Tuple

from pydantic import Field
from datetime import datetime, date

from Hospital_System.domain.value_object import Number


class QueueService:
    def get_next_number(self, last_number:Number, current_date: date, time_now: datetime) -> Tuple[Number,date, datetime]:
        return Number(id=last_number.id + 1), current_date, time_now