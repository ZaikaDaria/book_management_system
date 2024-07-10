from sqlalchemy.orm import Session
from typing import List, Optional

from .schemas import BookCreate
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
