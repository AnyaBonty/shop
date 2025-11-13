from fastapi import APIRouter, Depends,status, HTTPException,Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.app.db.session import get_db
from backend.app.schemas.user import UserCreate
from backend.app.crud.user import *

router=APIRouter(prefix="/user", tags=["/v1/user"])

db_session=Annotated[AsyncSession, Depends(get_db)]


@router.post("/create",
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

@router.get('/',
            response_model=list[UserRead],
            status_code=status.HTTP_200_OK,
            summary='Получение списка пользователей')
async def get_users_endpoint(db: db_session, skip: int = 0, limit: int = 100):
    result=await get_users(db,skip,limit)
    return result

@router.put("/{user_id}",
            response_model=UserRead,
            status_code=status.HTTP_200_OK,
            summary='Изменение информации пользователя по id')
async def update_user_endpoint(db: db_session,user_id:int,updated_user:UserUpdate):
    await get_user_endpoint(user_id,db)
    user=await update_user(db,user_id,updated_user)
    return user

