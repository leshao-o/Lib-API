from src.services.base import BaseService
from src.schemas.author import AuthorAdd, AuthorPatch


class AuthorService(BaseService):
    async def create_author(self, author_data: AuthorAdd) -> AuthorAdd:
        new_author = await self.db.author.create(data=author_data)
        await self.db.commit()
        return new_author

    async def get_authors(self) -> list[AuthorAdd]:
        return await self.db.author.get_all()

    async def get_author_by_id(self, id: int) -> AuthorAdd:
        return await self.db.author.get_by_id(id=id)

    async def edit_author(self, id: int, author_data: AuthorPatch) -> AuthorAdd:
        edited_author = await self.db.author.update(id=id, data=author_data)
        await self.db.commit()
        return edited_author
    
    async def delete_author(self, id: int) -> AuthorAdd:
        deleted_author = await self.db.author.delete(id=id)
        await self.db.commit()
        return deleted_author
