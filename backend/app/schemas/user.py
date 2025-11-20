from pydantic import BaseModel, constr
from datetime import datetime

class UserBase(BaseModel):
    first_name: str|None
    last_name: str|None
    email: str
    phone: str|None = None



class UserCreate(UserBase):
    password: constr(min_length=6, max_length=50)

class UserRead(UserBase):
    id: int
    is_superuser: bool
    role_id: int
    class Config:
        from_attributes = True
        extra = "ignore" #игнорирование лишних полей в схеме

class UserUpdate(UserBase):
    password: str | None

class UsersRead(BaseModel):
    users: list[UserRead]

class UserLogin(BaseModel):
    username: str
    password: constr(min_length=6, max_length=50)
