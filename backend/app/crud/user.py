from typing import Any, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.schemas.user import UserRead, UserCreate, UserUpdate
from backend.app.models import User


async def get_user(db: AsyncSession, user_id:int):
    result  =await db.execute(select(User).where(User.id ==user_id ))
    return result .scalar_one_or_none()

async def get_user_by_phone(db: AsyncSession, phone: str):
    result = await db.execute(select(User).where(User.phone == phone))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
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


async def update_user(db: AsyncSession,user_id:int, user: UserUpdate):
    result=await db.execute(select(User).where(User.id == user_id))
    db_user=result.scalar_one_or_none()
    if not db_user:
        return None
    db_user.email=user.email
    db_user.hashed_password=user.hashed_password
    db_user.phone=user.phone
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user=result.scalar_one_or_none()
    if not db_user:
        return None
    await db.delete(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

