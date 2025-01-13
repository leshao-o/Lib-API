from datetime import date

from pydantic import BaseModel


class UserAdd(BaseModel):
    name: str
    email: str
    hashed_password: str
    is_user: bool
    is_admin: bool

class User(UserAdd):
    id: int
