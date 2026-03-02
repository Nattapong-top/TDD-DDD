# Domain Logic for Library_System
from datetime import timedelta, date

from pydantic import BaseModel, Field


class BookNotBorrowedError(ValueError): pass


class BookAlreadyBorrowedBook(ValueError): pass

class Book(BaseModel):
    isbn: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    barcode: str = Field(..., min_length=1)


class Member(BaseModel):
    name: str = Field(..., min_length=1)


class LoanRecord(BaseModel):
    member_name: str = Field(..., min_length=1)
    borrowed_date: date

class LibrarySystem:
    def __init__(self):
        self._borrowed_books: dict[str, LoanRecord] = {} # Barcode: LoanRecord
        self._fine_per_day = 10
        self._loan_duration_days = 3

    def borrow(self, book: Book, member: Member, borrow_date: date = None) -> tuple[str, str]:
        if borrow_date is None:
            borrow_date = date.today()
        self._validate_book(book)
        self._borrowed_books[book.barcode] = LoanRecord(
            member_name=member.name,
            borrowed_date=borrow_date,
        )
        return book.title, member.name

    def return_book(self, book: Book, return_date: date) -> tuple[str, str, int]:
        if not self.is_borrowed(book):
            raise BookNotBorrowedError
        loan = self._borrowed_books.pop(book.barcode)
        fine = self._calculate_fine(return_date=return_date, borrow_date=loan.borrowed_date)

        return book.title, loan.member_name, fine

    def _calculate_fine(self, borrow_date: date, return_date: date) -> int:
        due_date = borrow_date + timedelta(days=self._loan_duration_days)
        # ลอง print ออกมาดูในขณะรันเทสก็ได้ครับป๋า
        # print(f"DEBUG: Due was {due_date}, Return was {return_date}")
        days_late = (return_date - due_date).days
        return max(0, days_late * self._fine_per_day)

    def is_borrowed(self, book: Book) -> bool:
        return book.barcode in self._borrowed_books

    def _validate_book(self, book: Book) -> None:
        if book.barcode in self._borrowed_books:
            raise BookAlreadyBorrowedBook

    def get_borrowed_count(self) -> int:
        return len(self._borrowed_books)
