from pydantic import BaseModel, EmailStr


class UserAdd(BaseModel):
    name: str
    email: str
    hashed_password: str


class UserPatch(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    

class UserRequestAdd(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    borrowed_books: int
    is_user: bool
    is_admin: bool


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserAdd):
    id: int
    borrowed_books: int
    is_user: bool
    is_admin: bool
