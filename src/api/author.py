from fastapi import APIRouter, Body

from src.exceptions import (
    AuthorNotFoundException,
    AuthorNotFoundHTTPException,
    InvalidInputException,
    InvalidInputHTTPException,
)
from src.services.author import AuthorService
from src.api.dependencies import DBDep, PaginationDep, AdminUserDep
from src.schemas.author import AuthorAdd, AuthorPatch
from src.logger import logger


router = APIRouter(prefix="/authors", tags=["Авторы"])


@router.post(
    "",
    summary="Добавляет автора",
    description=(
        """Этот эндпоинт добавляет нового автора в базу данных. 
        Ожидает имя, биорафию и дату рождения автора. 
        Возвращает статус операции и данные нового автора."""
    ),
)
async def add_author(
    db: DBDep,
    admin_user: AdminUserDep,
    author_data: AuthorAdd = Body(
        openapi_examples={
            "1": {
                "summary": "author_1",
                "value": {
                    "name": "Александр Пушкин",
                    "biography": "Один из самых авторитетных литературных деятелей первой трети XIX века. Ещё при жизни Пушкина сложилась его репутация величайшего национального русского поэта. Пушкин рассматривается как основоположник современного русского литературного языка.",
                    "birth_date": "1799-06-06",
                },
            },
            "2": {
                "summary": "author_2",
                "value": {
                    "name": "Лев Толстой",
                    "biography": "Писатель, ещё при жизни признанный главой русской литературы. Один из наиболее известных русских писателей и мыслителей, один из величайших в мире писателей-романистов.",
                    "birth_date": "1828-09-09",
                },
            },
        }
    ),
):
    logger.info("Добавление автора")
    new_author = await AuthorService(db).create_author(author_data=author_data)
    logger.info("Автор добавлен успешно")
    return {"status": "OK", "data": new_author}


@router.get(
    "",
    summary="Возвращает список всех авторов",
    description=(
        """Этот эндпоинт возвращает список всех авторов из базы данных со страничной пагинацией. 
        Ожидает количество авторов на странице и номер страницы. 
        Возвращает статус операции и данные авторов для указанной страницы."""
    ),
)
async def get_authors(db: DBDep, admin_user: AdminUserDep, pagination: PaginationDep):
    logger.info("Получение списка авторов")
    authors = await AuthorService(db).get_authors()
    authors = authors[pagination.per_page * (pagination.page - 1) :][: pagination.per_page]
    logger.info("Список авторов получен успешно")
    return {"status": "OK", "data": authors}


@router.get(
    "/{id}",
    summary="Возвращает данные конкретного автора",
    description=(
        """Этот эндпоинт возвращает информацию об авторе по его id. 
        Ожидает id автора. 
        Возвращает статус операции и данные запрашиваемого автора."""
    ),
)
async def get_author_by_id(db: DBDep, admin_user: AdminUserDep, id: int):
    logger.info("Получение автора по id")
    try:
        author = await AuthorService(db).get_author_by_id(id=id)
        logger.info("Автор получен успешно")
    except AuthorNotFoundException:
        logger.error("Автор не найден")
        raise AuthorNotFoundHTTPException
    return {"status": "OK", "data": author}


@router.put(
    "/{id}",
    summary="Обновляет данные конкретного автора",
    description=(
        """Этот эндпоинт редактирует информацию об авторе по его id. 
        Ожидает id автора и необязательные данные для обновления: имя, биографию и дату рождения. 
        Возвращает статус операции и данные автора c обновленными значениями."""
    ),
)
async def edit_author(
    db: DBDep,
    id: int,
    admin_user: AdminUserDep,
    author_data: AuthorPatch = Body(
        openapi_examples={
            "1": {
                "summary": "author_1",
                "value": {"name": "Александр Грибоедов", "birth_date": "1795-01-15"},
            },
            "2": {
                "summary": "author_2",
                "value": {"biography": "новая биография"},
            },
        }
    ),
):
    logger.info(f"Обновление данных автора с id: {id}")
    try:
        edited_author = await AuthorService(db).edit_author(id=id, author_data=author_data)
        logger.info("Данные автора обновлены успешно")
    except InvalidInputException:
        logger.error("Ошибка обновления данных автора: неверный ввод")
        raise InvalidInputHTTPException
    except AuthorNotFoundException:
        logger.error(f"Автор с id {id} не найден")
        raise AuthorNotFoundHTTPException
    return {"status": "OK", "data": edited_author}


@router.delete(
    "/{id}",
    summary="Удаляет автора по его id",
    description=(
        """Этот эндпоинт удаляет автора из базы данных по его id. 
        Ожидает id автора. 
        Возвращает статус операции и данные удаленного автора."""
    ),
)
async def delete_author(db: DBDep, admin_user: AdminUserDep, id: int):
    logger.info(f"Удаление автора с id: {id}")
    try:
        deleted_author = await AuthorService(db).delete_author(id=id)
        logger.info(f"Автор с id {id} удален успешно")
    except AuthorNotFoundException:
        logger.error(f"Автор с id {id} не найден")
        raise AuthorNotFoundHTTPException
    return {"status": "OK", "data": deleted_author}
