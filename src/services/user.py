from fastapi import HTTPException, Request, Response

from src.services.auth import AuthService
from src.schemas.user import User, UserAdd, UserLogin, UserPatch, UserRequestAdd, UserResponse
from src.services.base import BaseService


class UserService(BaseService):
    async def register_user(self, user_data: UserRequestAdd) -> User:
        hashed_password = AuthService().hash_password(user_data.password)
        new_user_data = UserAdd(
            name=user_data.name, email=user_data.email, hashed_password=hashed_password
        )
        new_user = await self.db.user.create(data=new_user_data)
        await self.db.commit()
        return new_user

    async def login_user(self, user_data: UserLogin, response: Response) -> str:
        user = await self.db.user.get_user_by_email(user_data.email)
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователем с таким email не зарегестрирован"
            )
        if not AuthService().verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неправильный пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token, httponly=True)
        return {"access_token": access_token}

    async def logout_user(self, request: Request, response: Response) -> None:
        if not request.cookies.get("access_token"):
            raise HTTPException(status_code=400, detail="Вы уже разлогинены")
        response.delete_cookie("access_token")

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.db.user.get_by_id(user_id)
        return UserResponse(**user.model_dump())

    async def get_all_users(self) -> list[UserResponse]:
        users = await self.db.user.get_all()
        users_response = []
        for i in range(len(users)):
            users_response.append(UserResponse(**users[i].model_dump()))
        return users_response
    
    async def edit_user(self, user_data: UserPatch, id: int) -> UserResponse:
        edited_user = await self.db.user.update(id=id, data=user_data)
        await self.db.commit()
        return UserResponse(**edited_user.model_dump())
