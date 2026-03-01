import pytest
from pydantic import ValidationError

from Loan_System.domain.loan_logic import (
    LoanSystem, Employee, Asset, MockDateProvider, AssetAlreadyBorrowedError)

def test_should_return_success_message_when_loan_successfully():
    mock_date = MockDateProvider()
    system = LoanSystem(date_provider=mock_date)
    emp = Employee(name='ณัฐพงศ์', dept='IT')
    asset = Asset(serial_no='NB-001', model='Dell Latitude')
    result = system.borrow(asset, emp)
    assert result == f'ณัฐพงศ์ (IT) Borrowed {asset.model} {asset.serial_no} on {mock_date.__call__()}'

def test_should_raise_error_when_borrowing_already_loaned_asset():
    mock_date = MockDateProvider()
    system = LoanSystem(date_provider=mock_date)

    asset = Asset(serial_no='NB-001', model='Dell Latitude')
    emp1 = Employee(name='ณัฐพงศ์', dept='IT')
    emp2 = Employee(name='จุกทอง', dept='Developer')

    system.borrow(asset, emp1)

    with pytest.raises(AssetAlreadyBorrowedError):
        system.borrow(asset, emp2)

def test_should_raise_error_when_employee_name_is_empty():
    with pytest.raises(ValidationError):
        Employee(name='', dept='IT')

def test_should_raise_error_when_asset_is_empty():
    with pytest.raises(ValidationError):
        Asset(serial_no='', model='Dell Latitude')


def test_should_allow_return_asset_successfully():
    mock_date = MockDateProvider()
    system = LoanSystem(date_provider=mock_date)
    asset = Asset(serial_no='NB-001', model='Dell Latitude')
    emp =  Employee(name='ณํฐพงศ์', dept='IT')
    system.borrow(asset, emp)
    system.return_asset(asset)

    result = system.borrow(asset, emp)
    assert 'Borrowed' in result

