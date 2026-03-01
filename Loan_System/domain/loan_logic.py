from pydantic import BaseModel, Field

class Employee(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description='Employee name ห้ามว่าง' )
    dept: str

class Asset(BaseModel):
    serial_no: str = Field(..., min_length=1, max_length=20, description='Asset Serial No ห้ามว่าง')
    model: str = Field(..., min_length=1, max_length=20, description='Asset Model ห้ามว่าง')

class AssetAlreadyBorrowedError(ValueError): pass

class AssetNotBorrowedError(ValueError): pass

class LoanLimitExceededError(ValueError): pass

def _format_loan_message(emp: Employee, asset: Asset, date:str) -> str:
    return f'{emp.name} ({emp.dept}) Borrowed {asset.model} {asset.serial_no} on {date}'


class LoanSystem:

    def __init__(self, date_provider):
        self._date_provider = date_provider
        self._active_loans = {}

    def borrow(self, asset: Asset, emp:Employee) -> str:
        self._validate_asset_availability(asset)
        self._get_borrowed_count(emp)
        self._active_loans[asset.serial_no] = emp.name
        return _format_loan_message(emp, asset, self._get_current_date())

    def _get_borrowed_count(self, emp: Employee):
        borrowed_count = list(self._active_loans.values()).count(emp.name)
        if borrowed_count >= 3:
            raise LoanLimitExceededError()

    def return_asset(self, asset: Asset) -> None:
        if not self._is_borrowed(asset):
            raise AssetNotBorrowedError()
        del self._active_loans[asset.serial_no]

    def get_borrower_name(self, asset: Asset) -> str:
        if not self._is_borrowed(asset):
            return 'No one'
        return self._active_loans[asset.serial_no]

    def get_loan_count(self) -> int:
        return len(self._active_loans)

    def _validate_asset_availability(self, asset: Asset):
        if self._is_borrowed(asset):
            raise AssetAlreadyBorrowedError()

    def _is_borrowed(self, asset: Asset) -> bool:
        return asset.serial_no in self._active_loans

    def _get_current_date(self) -> str:
        return self._date_provider()


class MockDateProvider:
    def __call__(self):
        return '2026-03-01'
