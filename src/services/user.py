from src.exceptions import InvalidInputException, ObjectNotFoundException, UserNotFoundException
from src.schemas.user import UserPatch, UserResponse
from src.services.base import BaseService


class UserService(BaseService):
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        try:
            user = await self.db.user.get_by_id(user_id)
            return UserResponse(**user.model_dump())
        except ObjectNotFoundException:
            raise UserNotFoundException

    async def get_all_users(self) -> list[UserResponse]:
        try:
            users = await self.db.user.get_all()
            users_response = []
            for i in range(len(users)):
                users_response.append(UserResponse(**users[i].model_dump()))
            return users_response
        except ObjectNotFoundException:
            raise UserNotFoundException

    async def edit_user(self, user_data: UserPatch, id: int) -> UserResponse:
        try:
            edited_user = await self.db.user.update(id=id, data=user_data)
        except InvalidInputException:
            raise InvalidInputException
        await self.db.commit()
        return UserResponse(**edited_user.model_dump())
