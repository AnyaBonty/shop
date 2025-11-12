from pydantic import BaseModel

class UserBase(BaseModel):
    email: str|None = None
    phone: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    password: str
