from datetime import date

from pydantic import BaseModel


class AuthorAdd(BaseModel):
    name: str
    biography: str
    birth_date: date


class AuthorPatch(BaseModel):
    name: str | None = None
    biography: str | None = None
    birth_date: date | None = None


class Author(AuthorAdd):
    id: int
