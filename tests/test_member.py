import pytest
from domain.models import EntiryTest


def test_check_super_is_working():
    obj = EntiryTest(name='ณัฐพงศ์')
    assert obj.version == 1
    assert obj.name == 'ณัฐพงศ์'
    obj.trigger_test()
    assert obj.version == 2