from typing import Any, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime,timezone

from sqlalchemy.orm import selectinload

from backend.app.schemas.role import RoleRead
from backend.app.schemas.user import UserRead, UserCreate, UserUpdate, UsersRead
from backend.app.models import User
from backend.app.core.security import *


async def get_user(db: AsyncSession, user_id:int):
    result  =await db.execute(select(User).where(User.id ==user_id ))
    return result .scalar_one_or_none()

async def get_user_by_phone(db: AsyncSession, phone: str):
    result = await db.execute(select(User).where(User.phone == phone))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).options(selectinload(User.role)).where(User.email == email))
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result_db = await db.execute(select(User).offset(skip).limit(limit))
    users= result_db.scalars().all()
    result = [UserRead.model_validate(user) for user in users]
    return result




async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email,phone=user.phone,hashed_password=hashed_password,
                   first_name=user.first_name,last_name=user.last_name,
                   created_at=datetime.now(timezone.utc),updated_at=datetime.now(timezone.utc))
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
    db_user.hashed_password=hash_password(user.password)
    db_user.phone=user.phone
    db_user.first_name=user.first_name
    db_user.last_name=user.last_name
    db_user.updated_at=datetime.now(timezone.utc)
    db_user.role=user.role
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user=result.scalar_one_or_none()
    if not db_user:
        return None

    db_user.is_active=False
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserRead.model_validate(db_user)


async def update_user_role(db: AsyncSession, user_id: int, role_id:int):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return None
    db_user.role_id=role_id

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserRead.model_validate(db_user)
