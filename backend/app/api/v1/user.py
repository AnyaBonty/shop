from fastapi import APIRouter, Depends, status, HTTPException, Body, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.app.api.v1.dependencies import get_current_user
from backend.app.core.jwt import decode_access_token
from backend.app.db.session import get_db
from backend.app.schemas.user import UserCreate
from backend.app.crud.user import *
from backend.app.api.v1.dependencies import oauth2_scheme, require_roles

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

@router.get("/me",
            summary='Получить свой id и роль')
async def read_me(token: str = Depends(oauth2_scheme)):
    user= await decode_access_token(token)

    return {"user": user['user_id'],
            'role': user['role']}

@router.get('/all',
            response_model=list[UserRead],
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_roles('admin'))],
            summary='Получение списка пользователей')
async def get_users_endpoint(db: db_session, skip: int = 0, limit: int = 100):
    result=await get_users(db,skip,limit)
    return result


@router.get("/{user_id}",
            response_model=UserRead,
            status_code=status.HTTP_200_OK,
            summary='Получение пользователя по id')
async def get_user_endpoint(user_id:int,db: db_session, payload: dict = Depends(require_roles("admin",'user'))):
    if payload.get('user_id') == user_id or payload.get('role')=='admin':
        read_user=await get_user(db,user_id) #Проверка наличия пользователя с данным id
        if read_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Пользователя с этим id не существует')
        return read_user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Нет прав доступа')



@router.put("/{user_id}",
            response_model=UserRead,
            status_code=status.HTTP_200_OK,
            summary='Изменение информации пользователя по id')
async def update_user_endpoint(db: db_session,user_id:int,updated_user:UserUpdate,payload: dict = Depends(require_roles("admin",'user'))):
    if payload.get('user_id') == user_id or payload.get('role') == 'admin':
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
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Нет прав доступа')

@router.delete("/",
               response_model=UserRead,
               status_code=status.HTTP_200_OK,
               dependencies=[Depends(require_roles('admin'))],
               summary='Удалить пользователя по id')
async def delete_user_endpoint(db: db_session,user_id:int):
    user=await delete_user(db,user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователя с этим id не существует')
    return user


@router.put('/{user_id}/{role_id}',
            response_model=UserRead,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_roles('admin'))],
            summary='Изменение роли пользователя')
async def update_role_endpoint(db:db_session,user_id:int,role_id:int):
    user=await update_user_role(db,user_id,role_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователя с этим id не существует')
    return user