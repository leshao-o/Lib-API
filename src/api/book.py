from fastapi import APIRouter, Body

from src.exceptions import (
    BookNotFoundException,
    BookNotFoundHTTPException,
    InvalidInputException,
    InvalidInputHTTPException,
    ObjectNotFoundException,
    ObjectNotFoundHTTPException,
)
from src.services.book import BookService
from src.api.dependencies import DBDep, PaginationDep, AdminUserDep, UserDep
from src.schemas.book import BookAddRequest, BookPatchRequest
from src.logger import logger


router = APIRouter(prefix="/books", tags=["Книги"])


@router.post(
    "",
    summary="Добавляет новую книгу",
    description=(
        """Этот эндпоинт добавляет новую книгу в базу данных. 
        Ожидает данные о книге, название, описание, id автора/авторов, количество доступных копий, дата публикации и жанр. 
        Возвращает статус операции и данные добавленной книги."""
    ),
)
async def add_book(
    db: DBDep,
    admin_user: AdminUserDep,
    book_data: BookAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "book_1",
                "value": {
                    "title": "Евгений Онегин",
                    "description": "Первый русский роман в стихах",
                    "author_ids": [1],
                    "available_copies": 5,
                    "date_of_publication": "1833-04-02",
                    "genre": "Роман в стихах",
                },
            },
            "2": {
                "summary": "book_2",
                "value": {
                    "title": "Капитанская дочка",
                    "description": "",
                    "author_ids": [1],
                    "available_copies": 4,
                    "date_of_publication": "1833-11-01",
                    "genre": "Исторический роман",
                },
            },
            "3": {
                "summary": "book_3",
                "value": {
                    "title": "Война и мир",
                    "description": "Очень длинная книга",
                    "author_ids": [2],
                    "available_copies": 8,
                    "date_of_publication": "1833-04-02",
                    "genre": "Роман-эпопея",
                },
            },
        }
    ),
):
    logger.info("Добавление новой книги")
    try:
        new_book = await BookService(db).create_book(book_data=book_data)
        logger.info("Книга добавлена успешно")
    except InvalidInputException:
        logger.error("Ошибка добавления книги: неверный ввод")
        raise InvalidInputHTTPException
    return {"status": "OK", "data": new_book}


@router.get(
    "",
    summary="Возвращает список всех книг",
    description=(
        """Этот эндпоинт возвращает список всех книг из базы данных со страничной пагинацией. 
        Ожидает количество книг на странице и номер страницы. 
        Возвращает статус операции и данные книг для указанной страницы."""
    ),
)
async def get_books(db: DBDep, user: UserDep, pagination: PaginationDep):
    logger.info("Получение списка книг")
    books = await BookService(db).get_books()
    books = books[pagination.per_page * (pagination.page - 1) :][: pagination.per_page]
    logger.info("Список книг получен успешно")
    return {"status": "OK", "data": books}


@router.get(
    "/{id}",
    summary="Возвращает книгу по id",
    description=(
        """Этот эндпоинт возвращает информацию о книге по её id. 
        Ожидает ID книги. 
        Возвращает статус операции и данные запрашиваемой книги."""
    ),
)
async def get_book_by_id(user: UserDep, db: DBDep, id: int):
    logger.info(f"Получение книги по id: {id}")
    try:
        book = await BookService(db).get_book_by_id(id=id)
        logger.info("Книга получена успешно")
    except ObjectNotFoundException:
        logger.error("Книга не найдена")
        raise ObjectNotFoundHTTPException
    return {"status": "OK", "data": book}


@router.put(
    "/{id}",
    summary="Редактирует книгу",
    description=(
        """Этот эндпоинт редактирует информацию о книге по её уникальному идентификатору. 
        Ожидает ID книги и необязательные данные для обновления: название, описание, ID автора и количество доступных копий. 
        Возвращает статус операции и обновленные данные книги."""
    ),
)
async def edit_book(
    db: DBDep,
    admin_user: AdminUserDep,
    id: int,
    book_data: BookPatchRequest = Body(
        openapi_examples={
            "1": {
                "summary": "book_1",
                "value": {
                    "title": "Евгений Онегин",
                    "description": "'ЕВГЕНИЙ ОНЕГИН' — первый русский роман в стихах",
                    "author_ids": [2, 3],
                    "available_copies": 10,
                    "date_of_publication": "1888-04-02",
                    "genre": "Роман",
                },
            },
            "2": {
                "summary": "book_2",
                "value": {"available_copies": 7},
            },
            "3": {
                "summary": "book_3",
                "value": {"description": "Книга"},
            },
        }
    ),
):
    logger.info(f"Редактирование книги с id: {id}")
    try:
        edited_book = await BookService(db).edit_book(id=id, book_data=book_data)
        logger.info(f"Книга с id: {id} успешно отредактирована")
    except BookNotFoundException:
        logger.error(f"Книга с id: {id} не найдена")
        raise BookNotFoundHTTPException
    except InvalidInputException:
        logger.error("Ошибка редактирования книги: неверный ввод")
        raise InvalidInputHTTPException
    return {"status": "OK", "data": edited_book}


@router.delete(
    "/{id}",
    summary="Удаляет книгу",
    description=(
        """Этот эндпоинт удаляет книгу из базы данных по её id. 
        Ожидает id книги. 
        Возвращает статус операции и данные удалённой книги."""
    ),
)
async def delete_book(db: DBDep, admin_user: AdminUserDep, id: int):
    logger.info(f"Удаление книги с id: {id}")
    try:
        deleted_book = await BookService(db).delete_book(id=id)
        logger.info(f"Книга с id: {id} успешно удалена")
    except BookNotFoundException:
        logger.error(f"Книга с id: {id} не найдена")
        raise BookNotFoundHTTPException
    return {"status": "OK", "data": deleted_book}
