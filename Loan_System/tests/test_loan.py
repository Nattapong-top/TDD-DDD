import pytest
from pydantic import ValidationError

from Loan_System.domain.loan_logic import (
    LoanSystem, Employee, Asset, MockDateProvider, AssetAlreadyBorrowedError,
    AssetNotBorrowedError, LoanLimitExceededError)

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

def test_should_raise_error_when_returning_asset_that_was_not_borrowed():
    mock_date = MockDateProvider()
    system = LoanSystem(date_provider=mock_date)
    asset = Asset(serial_no='Ghost-000', model='No Brand')

    with pytest.raises(AssetNotBorrowedError):
        system.return_asset(asset)


def test_should_return_employee_name_who_borrowed_the_asset():
    system = LoanSystem(MockDateProvider())
    asset = Asset(serial_no='NB-002', model='Macbook')
    emp = Employee(name='ณัฐพงศ์', dept='IT')
    system.borrow(asset, emp)

    borrower = system.get_borrower_name(asset)
    assert borrower == emp.name

def test_should_return_correct_count_of_active_loans():
    system = LoanSystem(MockDateProvider())
    system.borrow(Asset(serial_no='NB-001', model='Dell Latitude'), Employee(name='ณัฐพงศ์', dept='IT'))
    system.borrow(Asset(serial_no='NB-002', model='MacBook'), Employee(name='นามสมมุติ', dept='OP'))

    assert system.get_loan_count() == 2

def test_should_raise_error_when_employee_borrows_more_than_three_items():
    system = LoanSystem(MockDateProvider())
    emp = Employee(name='ณัฐพงศ์', dept='IT')

    system.borrow(Asset(serial_no='NB-001', model='Dell Latitude'), emp)
    system.borrow(Asset(serial_no='NB-002', model='Dell Latitude'), emp)
    system.borrow(Asset(serial_no='NB-003', model='Dell Latitude'), emp)

    with pytest.raises(LoanLimitExceededError):
        system.borrow(Asset(serial_no='NB-004', model='Dell Latitude'), emp)

def test_should_record_correct_loan_date_from_provider():
    mock_date = MockDateProvider()
    mock_date.return_value = '2026-12-25'

    system = LoanSystem(date_provider=mock_date)
    asset = Asset(serial_no='XMAS-001', model='iPad')
    emp = Employee(name='ซานต้า', dept='TCD')

    result = system.borrow(asset, emp)
    assert '2026-12-25' in result