from datetime import date

from pydantic import BaseModel


class AuthorAdd(BaseModel):
    name: str
    biography: str
    birth_date: date

class Author(AuthorAdd):
    id: int
