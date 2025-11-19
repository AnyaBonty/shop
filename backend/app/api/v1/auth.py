from os import access
from typing import Annotated

from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.jwt import create_access_token
from backend.app.crud.user import get_user_by_email
from backend.app.db.session import get_db
from backend.app.schemas.user import UserLogin
from backend.app.core.security import verify_password
from backend.app.schemas.login import *

router=APIRouter(prefix="/auth", tags=["auth"])

db_sesson=Annotated[AsyncSession, Depends(get_db)]

@router.post("/login", response_model=LoginResponse,
             status_code=status.HTTP_201_CREATED)
async def login(db:db_sesson, user: UserLogin):
    db_user = await get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Некорректный пароль')
    body={"user_id": db_user.id, "role": db_user.role.name}
    access_token= create_access_token(body)
    return {"access_token": access_token, "token_type": "bearer"}