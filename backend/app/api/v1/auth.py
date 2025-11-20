
from typing import Annotated

from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.jwt import create_access_token, decode_access_token
from backend.app.core.redis import remove_token_from_redis
from backend.app.crud.auth import RegisterUser, create_user_register
from backend.app.crud.user import get_user_by_email, create_user
from backend.app.db.session import get_db
from backend.app.core.security import verify_password
from backend.app.schemas.login import *
from backend.app.api.v1.dependencies import oauth2_scheme
from backend.app.crud.user import delete_user


router=APIRouter(prefix="/auth", tags=["auth"])

db_session=Annotated[AsyncSession, Depends(get_db)]

@router.post("/login", response_model=LoginResponse,
             status_code=status.HTTP_201_CREATED)
async def login(db:db_session, form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = await get_user_by_email(db, form_data.username)

    if not db_user or not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь не найден")
    if not verify_password(form_data.password, db_user.hashed_password) :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Некорректный пароль')
    body={"user_id": db_user.id, "role": db_user.role.name}
    access_token= await create_access_token(body)
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/logout",
               status_code=status.HTTP_200_OK,)

async def logout(token: str = Depends(oauth2_scheme)):
    await remove_token_from_redis(token)
    return {"msg": "Successfully logged out"}



@router.post("/user",
            status_code=status.HTTP_201_CREATED)
async def register(db:db_session,user: RegisterUser):
    user_In_db= await get_user_by_email(db,user.email)
    if user_In_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Такой пользователь же существет'
                            )
    if user.password!=user.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Некорректный пароль')
    created_user = await create_user_register(db, user)
    return created_user


@router.delete("/delete_me",
               status_code=status.HTTP_200_OK,
               summary='Удалить свой аккаунт')

async def delete_user_by_token_endpoint(db:db_session,token: str = Depends(oauth2_scheme)):
    payload=await decode_access_token(token)
    delete_user_from_db=await delete_user(db,payload.get('user_id'))
    await remove_token_from_redis(token)
    return delete_user_from_db