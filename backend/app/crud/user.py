from typing import Any, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.schemas.user import UserRead, UserCreate, UserUpdate
from backend.app.models import User


async def get_user(db: AsyncSession, user_id:int) -> UserRead:
    result  =await db.execute(select(User).where(User.id ==user_id ))
    return result .scalar_one_or_none()

async def get_user_by_phone(db: AsyncSession, phone: str):
    result = await db.execute(select(User).where(User.phone == phone))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(email=user.email,phone=user.phone,hashed_password=user.hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
async def update_user(db: AsyncSession, user: UserUpdate):
    result=db.execute(select(User).where(User.id == user.id))
    db_user=result.scalar_one_or_none()