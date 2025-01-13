from datetime import date

from pydantic import BaseModel


class BookAdd(BaseModel):
    title: str
    description: str
    date_of_publication: date
    author_id: list[int] = []
    genre: str
    available_copies: int

class Book(BookAdd):
    id: int
