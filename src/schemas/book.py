from datetime import date

from pydantic import BaseModel

from src.schemas.author import Author


class BookAddRequest(BaseModel):
    title: str
    description: str
    date_of_publication: date
    author_ids: list[int] = []
    genre: str
    available_copies: int


class BookPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    date_of_publication: date | None = None
    author_ids: list[int] | None = None
    genre: str | None = None
    available_copies: int | None = None


class BookPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    date_of_publication: date | None = None
    genre: str | None = None
    available_copies: int | None = None


class BookAdd(BaseModel):
    title: str
    description: str
    date_of_publication: date
    genre: str
    available_copies: int


class Book(BookAdd):
    id: int


class BookWithRels(Book):
    authors: list[Author]


class BooksAuthorsAdd(BaseModel):
    book_id: int
    author_id: int


class BooksAuthors(BooksAuthorsAdd):
    id: int
