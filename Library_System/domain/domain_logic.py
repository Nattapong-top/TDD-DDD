# Domain Logic for Library_System
from pydantic import BaseModel, Field


class Book(BaseModel):
    isbn: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    barcode: str = Field(..., min_length=1)


class Member(BaseModel):
    name: str = Field(..., min_length=1)


class BookAlreadyBorrowedBook(ValueError): pass


class LibrarySystem:
    def __init__(self):
        self._borrowed_books = {}

    def borrow(self, book: Book, member: Member) -> tuple[str, str]:
        self._validate_book(book)

        self._borrowed_books[book.barcode] = member.name
        return book.title, member.name

    def _validate_book(self, book: Book):
        if book.barcode in self._borrowed_books:
            raise BookAlreadyBorrowedBook

    def get_borrowed_count(self) -> int:
        return len(self._borrowed_books)
