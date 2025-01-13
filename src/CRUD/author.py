from src.schemas.author import Author
from src.models.author import AuthorsORM
from src.CRUD.base import BaseCRUD


class AuthorCRUD(BaseCRUD):
    model = AuthorsORM
    schema = Author
