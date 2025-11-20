from fastapi import APIRouter, Depends, status, HTTPException, Body, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.app.api.v1.dependencies import get_current_user
from backend.app.db.session import get_db
from backend.app.schemas.user import UserCreate
from backend.app.crud.user import *
from fastapi.security import OAuth2PasswordBearer

router=APIRouter(prefix="/user", tags=["/v1/user"])

db_session=Annotated[AsyncSession, Depends(get_db)]


@router.post("/",
             response_model=UserRead,
             status_code=status.HTTP_201_CREATED,
             summary="Создать нового пользователя")
async def create_user_endpoint(user:Annotated[UserCreate,Body(...,description='Данные для создания пользователя')], db: db_session ):
    user_phone=await get_user_by_phone(db,user.phone)
    user_email=None
    if user.email:
        user_email=await get_user_by_email(db,user.email)

    if user_phone or user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Пользователь с таким телефоном или email уже существует')
    created_user=await create_user(db,user)
    return created_user

@router.get("/me")
async def read_me(authorization: str = Header(..., alias="Authorization")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid header")
    token = authorization.split(" ")[1]
    return {"token": token}

@router.get('/all',
            response_model=list[UserRead],
            status_code=status.HTTP_200_OK,
            summary='Получение списка пользователей')
async def get_users_endpoint(db: db_session, skip: int = 0, limit: int = 100):
    result=await get_users(db,skip,limit)
    return result


@router.get("/{user_id}",
            response_model=UserRead,
            status_code=status.HTTP_200_OK,
            summary='Получение пользователя по id')
async def get_user_endpoint(user_id:int,db: db_session):
    read_user=await get_user(db,user_id) #Проверка наличия пользователя с данным id
    if read_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователя с этим id не существует')
    return read_user



@router.put("/{user_id}",
            response_model=UserRead,
            status_code=status.HTTP_200_OK,
            summary='Изменение информации пользователя по id')
async def update_user_endpoint(db: db_session,user_id:int,updated_user:UserUpdate):
    read_user = await get_user(db, user_id)  # Проверка наличия пользователя с данным id
    email_user=await get_user_by_email(db,updated_user.email) # Проверка наличия пользователя с данным email (сам пользователь не учитывается)
    phone_user=await get_user_by_phone(db,updated_user.phone) # Проверка наличия пользователя с данным телефоном (сам пользователь не учитывается)
    if (email_user and email_user.id!=user_id) or (phone_user and phone_user.id!=user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Пользователь с таким телефоном или email уже существует')

    if read_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователя с этим id не существует')
    user=await update_user(db,user_id,updated_user)
    return user

@router.delete("/",
               response_model=UserRead,
                status_code=status.HTTP_200_OK,
               summary='Удалить пользователя по id')
async def delete_user_endpoint(db: db_session,user_id:int):
    user=await delete_user(db,user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователя с этим id не существует')
    return user