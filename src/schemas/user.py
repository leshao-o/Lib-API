from pydantic import BaseModel, EmailStr


class UserAdd(BaseModel):
    name: str
    email: str
    hashed_password: str


class UserRequestAdd(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class User(UserAdd):
    id: int
    is_user: bool
    is_admin: bool