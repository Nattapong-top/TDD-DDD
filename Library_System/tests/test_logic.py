# Unit Tests for Library_System
import pytest
from Library_System.domain.domain_logic import LibrarySystem, Book, Member, BookAlreadyBorrowedBook, \
    BookNotBorrowedError


def test_should_return_success_message_when_borrow_successfully():
    system = LibrarySystem()
    book = Book(isbn='978-1', title='Clean Architecture', barcode='BC-001')
    member = Member(name='ณัฐพงศ์')
    result = system.borrow(book, member)
    assert 'ณัฐพงศ์' in result
    assert 'Clean Architecture' in result


def test_should_raise_error_when_borrowing_already_borrowed_book():
    system = LibrarySystem()
    book = Book(isbn='978-1', title='Clean Architecture', barcode='BC-001')
    member = Member(name='nattapong')
    member2 = Member(name='jungthon')
    system.borrow(book, member)
    with pytest.raises(BookAlreadyBorrowedBook):
        system.borrow(book, member2)


def test_should_allow_borrowing_different_copies_of_the_same_book():
    system = LibrarySystem()
    member = Member(name='nattapong')
    member2 = Member(name='jungthon')
    copy1 = Book(isbn='978-1', title='Clean Architecture', barcode='BC-001')
    copy2 = Book(isbn='978-1', title='Clean Architecture', barcode='BC-002')
    system.borrow(copy1, member)
    system.borrow(copy2, member2)
    assert system.get_borrowed_count() == 2


def test_should_allow_returning_book_successfully():
    system = LibrarySystem()
    book = Book(isbn='978-1', title='Clean Architecture', barcode='BC-001')
    member = Member(name='nattapong')
    system.borrow(book, member)
    title, name = system.return_book(book)
    assert title == 'Clean Architecture'
    assert name == 'nattapong'
    assert system.get_borrowed_count() == 0


def test_should_raise_error_when_returning_book_that_was_not_borrowed():
    system = LibrarySystem()
    book = Book(isbn='978-1', title='Clean Architecture', barcode='BC-001')
    with pytest.raises(BookNotBorrowedError):
        system.return_book(book)