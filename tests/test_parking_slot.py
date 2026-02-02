import pytest
from domain.models import ParkingSlot


def test_parking_slot_cannot_occupy_if_already_taken():
    # 1. สร้างช่องจอด A1 ที่สถานะ 'ไม่ว่าง' (is_vacant=False)
    slot = ParkingSlot(slot_id='A1', is_vacant=False)
    # ลองจอดซ้ำ ต้องขึ้น error 
    with pytest.raises(ValueError):
        slot.occupy()
    