from pydantic import BaseModel

class UserBase(BaseModel):
    email: str|None = None
    phone: str

class UserCreate(UserBase):
    hashed_password: str

class UserRead(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    hashed_password: str
