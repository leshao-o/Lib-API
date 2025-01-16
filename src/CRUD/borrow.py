from src.schemas.borrow import Borrow
from src.models.borrow import BorrowsORM
from src.CRUD.base import BaseCRUD


class BorrowCRUD(BaseCRUD):
    model = BorrowsORM
    schema = Borrow
