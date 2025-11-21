from typing import Annotated

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.v1 import user,product,order,role,auth
from contextlib import asynccontextmanager

from backend.app.core.config import settings
from backend.app.core.security import hash_password
from backend.app.db.session import get_db
from backend.app.models import Role, User
from backend.app.db.session import SessionLocal

db_session=Annotated[AsyncSession,Depends(get_db)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Открываем сессию через твою фабрику SessionLocal
    async with SessionLocal() as db:
        # 1. Создаём 4 роли в нужном порядке
        desired_roles = [
            "user",  # ← id=1 → будет по умолчанию у новых пользователей
            "customer",
            "manager",
            "admin",  # ← для суперпользователя
        ]

        for role_name in desired_roles:
            result = await db.execute(select(Role).where(Role.name == role_name))
            if result.scalar_one_or_none() is None:
                db.add(Role(name=role_name))
                print(f"Создана роль: {role_name}")

        await db.commit()

        # 2. Создаём суперпользователя
        result = await db.execute(
            select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
        )
        if result.scalar_one_or_none() is None:
            admin_role_res = await db.execute(select(Role).where(Role.name == "admin"))
            admin_role = admin_role_res.scalar_one()

            superuser = User(
                email=settings.FIRST_SUPERUSER_EMAIL,
                hashed_password=hash_password(settings.FIRST_SUPERUSER_PASSWORD),
                first_name="Super",
                last_name="Admin",
                is_superuser=True,
                is_active=True,
                role_id=admin_role.id,
            )
            db.add(superuser)
            await db.commit()
            print(f"Создан суперпользователь: {settings.FIRST_SUPERUSER_EMAIL}")
        else:
            print("Суперпользователь уже существует")

    print("Lifespan завершён — роли и админ готовы!")
    yield
app = FastAPI(title="Shop API",
              lifespan=lifespan)


app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(role.router)
app.include_router(auth.router)

