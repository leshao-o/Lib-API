from datetime import date

from fastapi import APIRouter, Body

from src.exceptions import (
    BookAlreadyReturnedException,
    BookAlreadyReturnedHTTPException,
    BookNotFoundException,
    BookNotFoundHTTPException,
    MaxBooksLimitExceededException,
    MaxBooksLimitExceededHTTPException,
    NoAvailableCopiesException,
    NoAvailableCopiesHTTPException,
)
from src.services.borrow import BorrowService
from src.api.dependencies import DBDep, PaginationDep, UserDep, AdminUserDep
from src.schemas.borrow import BorrowAddRequest


router = APIRouter(prefix="/borrows", tags=["Выдачи"])


@router.post(
    "",
    summary="Добавляет новый займ",
    description=(
        """Этот эндпоинт добавляет новый займ в базу данных. 
        Ожидает id книги, имя читателя и дату займа. 
        Возвращает статус операции и данные нового займа."""
    ),
)
async def add_borrow(
    db: DBDep,
    user: UserDep,
    borrow_data: BorrowAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "borrow_1",
                "value": {"book_id": 1, "borrow_date": "2024-12-10", "return_date": "2025-01-01"},
            },
            "2": {
                "summary": "borrow_2",
                "value": {"book_id": 2, "borrow_date": "2024-12-13", "return_date": "2025-01-02"},
            },
        }
    ),
):
    try:
        new_borrow = await BorrowService(db).add_borrow(user=user, borrow_data=borrow_data)
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    except NoAvailableCopiesException:
        raise NoAvailableCopiesHTTPException
    except MaxBooksLimitExceededException:
        raise MaxBooksLimitExceededHTTPException
    return {"status": "OK", "data": new_borrow}


@router.get(
    "",
    summary="Возвращает список всех займов",
    description=(
        """Этот эндпоинт возвращает список всех займов из базы данных со страничной пагинацией. 
        Ожидает количество займов на странице и номер страницы. 
        Возвращает статус операции и данные займов для указанной страницы."""
    ),
)
async def get_borrows(db: DBDep, admin_user: AdminUserDep, pagin: PaginationDep):
    borrows = await BorrowService(db).get_borrows()
    borrows = borrows[pagin.per_page * (pagin.page - 1) :][: pagin.per_page]
    return {"status": "OK", "data": borrows}


@router.get(
    "/{id}",
    summary="Возвращает займы читателя",
    description=(
        """Этот эндпоинт возвращает информацию о займе читателя.  
        Возвращает статус операции и данные займов читателя."""
    ),
)
async def get_my_borrows(db: DBDep, user: UserDep):
    borrows = await BorrowService(db).get_my_borrows(user_id=user.id)
    return {"status": "OK", "data": borrows}


@router.patch(
    "/{id}/return",
    summary="Завершает займ книги",
    description=(
        """Этот эндпоинт позволяет вернуть книгу по его id займа. 
        Ожидает id займа и дату фактического возврата. 
        Возвращает статус операции и данные о возвращённом займе."""
    ),
)
async def return_book(db: DBDep, id: int, return_date: date, user: UserDep):
    try:
        returned_borrow = await BorrowService(db).return_book(
            id=id, return_date=return_date, user=user
        )
    except BookAlreadyReturnedException:
        raise BookAlreadyReturnedHTTPException
    return {"status": "OK", "data": returned_borrow}
