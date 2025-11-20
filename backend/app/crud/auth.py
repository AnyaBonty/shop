from datetime import datetime, timezone

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.security import hash_password
from backend.app.models import User


class RegisterUser(BaseModel):
    email: str
    password: str
    confirm_password: str
    first_name: str | None
    last_name: str | None
    phone: str | None = None



async def create_user_register(db: AsyncSession, user: RegisterUser):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email,phone=user.phone,hashed_password=hashed_password,
                   first_name=user.first_name,last_name=user.last_name,
                   created_at=datetime.now(timezone.utc),updated_at=datetime.now(timezone.utc))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user