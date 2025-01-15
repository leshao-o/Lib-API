from fastapi import HTTPException, Request, Response

from src.services.auth import AuthService
from src.schemas.user import User, UserAdd, UserLogin, UserRequestAdd
from src.services.base import BaseService


class UserService(BaseService):
    async def register_user(self, user_data: UserRequestAdd) -> User:
        hashed_password = AuthService().hash_password(user_data.password)
        new_user_data = UserAdd(name=user_data.name, email=user_data.email, hashed_password=hashed_password)
        new_user = await self.db.user.create(data=new_user_data)
        await self.db.commit()
        return new_user

    async def login_user(self, user_data: UserLogin, response: Response) -> str:
        user = await self.db.user.get_user_by_email(user_data.email)
        # сделать проверку на пароль и существование юзера по email
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    
    async def logout_user(self, request: Request, response: Response):
        if not request.cookies.get("access_token"): 
            # поменять ошибку на кастомную
            raise HTTPException(status_code=400, detail="Вы уже разлогинены")
        response.delete_cookie("access_token")

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.db.user.get_by_id(user_id)