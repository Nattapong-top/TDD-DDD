from pydantic import BaseModel, Field

class Employee(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description='Employee name ห้ามว่าง' )
    dept: str

class Asset(BaseModel):
    serial_no: str = Field(..., min_length=1, max_length=20, description='Asset Serial No ห้ามว่าง')
    model: str = Field(..., min_length=1, max_length=20, description='Asset Model ห้ามว่าง')

class AssetAlreadyBorrowedError(ValueError): pass

def _format_loan_message(emp: Employee, asset: Asset, date:str) -> str:
    return f'{emp.name} ({emp.dept}) borrowed {asset.model} {asset.serial_no} on {date}'


class LoanSystem:

    def __init__(self, date_provider):
        self._date_provider = date_provider
        self._active_loans = {}

    def borrow(self, asset: Asset, emp:Employee) -> str:
        self._validate_asset_availability(asset)

        self._active_loans[asset.serial_no] = emp.name

        loan_date = self._get_current_date()
        return _format_loan_message(emp, asset, loan_date)

    def _validate_asset_availability(self, asset: Asset):
        if asset.serial_no in self._active_loans:
            raise AssetAlreadyBorrowedError()

    def _get_current_date(self):
        return self._date_provider()


class MockDateProvider:
    def __call__(self):
        return '2026-03-01'