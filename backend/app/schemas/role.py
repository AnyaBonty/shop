from pydantic import BaseModel

from backend.app.schemas.user import UserRead


class RoleBase(BaseModel):
    name: str
    description: str | None = None

class RoleRead(RoleBase):
    id: int
    class Config:
        from_attributes = True

class RoleUpdate(BaseModel):
    name: str|None= None
    description: str|None = None

class RoleReadFull(RoleBase):
    id: int
    users:list[UserRead]
    class Config:
        from_attributes = True

