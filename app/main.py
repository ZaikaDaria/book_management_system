from datetime import date
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, database, models, schemas
from .database import SessionLocal

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_db() -> object:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/books/", response_class=HTMLResponse)
async def read_books(request: Request, db: Session = Depends(get_db)):
    books = crud.get_all_books(db=db)
    return templates.TemplateResponse("books.html", {"request": request, "books": books})


@app.get("/books/create", response_class=HTMLResponse)
async def create_book_form(request: Request):
    return templates.TemplateResponse("create_book_form.html", {"request": request})


@app.post("/books/create", response_model=schemas.Book, response_class=HTMLResponse)
async def create_book(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    publication_date: date = Form(...),
    isbn: str = Form(...),
    pages: int = Form(...),
    db: Session = Depends(get_db)
):
    book = schemas.BookCreate(
        title=title,
        author=author,
        publication_date=publication_date,
        isbn=isbn,
        pages=pages
    )
    created_book = crud.create_book(db=db, book=book)
    return templates.TemplateResponse("book_created.html", {"request": request, "book": created_book})


@app.get("/books/{book_id}", response_model=schemas.Book, response_class=HTMLResponse)
async def read_book(book_id: int, request: Request, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("book_detail.html", {"request": request, "book": book})


@app.get("/books/{book_id}/update", response_class=HTMLResponse)
async def update_book_form(book_id: int, request: Request, db: Session = Depends(get_db)):
    book = crud.get_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return templates.TemplateResponse("update_book_form.html", {"request": request, "book": book})


@app.post("/books/{book_id}/update", response_class=HTMLResponse)
async def update_book(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    publication_date: date = Form(...),
    isbn: str = Form(...),
    pages: int = Form(...),
    db: Session = Depends(get_db)
) -> schemas.Book:
    book_update = schemas.BookUpdate(
        title=title,
        author=author,
        publication_date=publication_date,
        isbn=isbn,
        pages=pages
    )
    updated_book = crud.update_book(db=db, book_id=book_id, book=book_update)
    return RedirectResponse(url=f"/books/{updated_book.id}", status_code=303)
