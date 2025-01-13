from src.schemas.book import Book
from src.models.book import BooksORM
from src.CRUD.base import BaseCRUD


class BookCRUD(BaseCRUD):
    model = BooksORM
    schema = Book
