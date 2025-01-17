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
from src.logger import logger


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
    logger.info("Добавление нового займа")
    try:
        new_borrow = await BorrowService(db).add_borrow(user=user, borrow_data=borrow_data)
        logger.info("Займ добавлен успешно")
    except BookNotFoundException:
        logger.error("Ошибка добавления займа: книга не найдена")
        raise BookNotFoundHTTPException
    except NoAvailableCopiesException:
        logger.error("Ошибка добавления займа: нет доступных копий книги")
        raise NoAvailableCopiesHTTPException
    except MaxBooksLimitExceededException:
        logger.error("Ошибка добавления займа: превышен лимит на количество книг")
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
    logger.info("Получение списка займов")
    borrows = await BorrowService(db).get_borrows()
    borrows = borrows[pagin.per_page * (pagin.page - 1) :][: pagin.per_page]
    logger.info("Список займов получен успешно")
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
    logger.info("Получение займов читателя")
    borrows = await BorrowService(db).get_my_borrows(user_id=user.id)
    logger.info("Займы читателя получены успешно")
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
    logger.info(f"Завершение займа книги с id: {id}")
    try:
        returned_borrow = await BorrowService(db).return_book(
            id=id, return_date=return_date, user=user
        )
        logger.info("Займ успешно завершён")
    except BookAlreadyReturnedException:
        logger.error("Займ уже был возвращён")
        raise BookAlreadyReturnedHTTPException
    return {"status": "OK", "data": returned_borrow}
