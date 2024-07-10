from sqlalchemy import Column, Date, Integer, String
from .database import Base


class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_date = Column(Date, index=True)
    isbn = Column(String(13), index=True)
    pages = Column(Integer, index=True)
