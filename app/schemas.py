from typing import List, Optional
from pydantic import BaseModel
from datetime import date


class BookBase(BaseModel):
    title: str
    author: str
    publication_date: date
    isbn: str
    pages: int


class BookCreate(BookBase):
    pass


class BookGet(BookBase):
    id: int
    title: str
    author: str
    publication_date: date
    isbn: str
    pages: int

    class Config:
        orm_mode = True


class PaginatedResponse(BaseModel):
    total: int
    items: List[BookGet]


class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    publication_date: Optional[date] = None
    isbn: Optional[str] = None
    pages: Optional[int] = None


class BookOut(BookBase):
    id: int
    title: str
    author: str
    publication_date: date
    isbn: str
    pages: int