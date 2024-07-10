from sqlalchemy.orm import Session
from typing import List, Optional

from .schemas import BookCreate, BookUpdate
from .models import DBBook


def get_all_books(
    db: Session,
) -> List[DBBook]:
    return db.query(DBBook).all()


def get_book(db: Session, book_id: int) -> Optional[DBBook]:
    return db.query(DBBook).filter(DBBook.id == book_id).first()


def create_book(db: Session, book: BookCreate) -> DBBook:
    db_book = DBBook(
        title=book.title,
        author=book.author,
        publication_date=book.publication_date,
        isbn=book.isbn,
        pages=book.pages,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: BookUpdate) -> DBBook:
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if db_book:
        for key, value in book.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> None:
    book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
