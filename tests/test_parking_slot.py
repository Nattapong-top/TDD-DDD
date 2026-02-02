import pytest
from domain.models import ParkingSlot


def test_parking_slot_behavior_and_versioning():
    # 1. เตรียมของ: สร้างช่องจอด A1 (ค่าเริ่มต้นต้องว่าง และ Version ต้องเป็น 1)
    slot = ParkingSlot(slot_id='A1')

    assert slot.is_vacant == True
    assert slot.version == 1

    # 2. ลงมือ: สั่งจอดรถ (occupy)
    slot.occupy()

    # 3. ฟันธง: สถานะต้องเปลี่ยน และ Version ต้องขยับเป็น 2!
    assert slot.is_vacant == False
    assert slot.version == 2

    # 4. ลองของ: สั่งจอดซ้ำในที่เดิม (ต้องโดนด่า)
    with pytest.raises(ValueError):
        slot.occupy()


def test_parking_slot_cannot_occupy_if_already_taken():
    # 1. สร้างช่องจอด A1 ที่สถานะ 'ไม่ว่าง' (is_vacant=False)
    slot = ParkingSlot(slot_id='A1', is_vacant=False)
    # ลองจอดซ้ำ ต้องขึ้น error 
    with pytest.raises(ValueError):
        slot.occupy()
    