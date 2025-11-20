from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.order import OrderCreate, OrderRead, OrderUpdate
from backend.app.crud.order import *
from backend.app.api.v1.dependencies import require_roles
router=APIRouter(prefix="/order", tags=["/v1/order"])

db_session=Annotated[AsyncSession, Depends(get_db)]

@router.post("/", response_model=OrderRead,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_roles('admin','manager'))],
             summary="Создание нового заказа для пользователя")
async def create_order_endpoint(db:db_session,request: OrderCreate):
    new_order=await create_order(db,request)
    return new_order


@router.get("/", response_model=OrderRead,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_roles('admin','manager'))],
            summary='Получение заказа по id')

async def get_order_by_id_endpoint(db:db_session,id:int):
    read_order=await get_order_by_id(db,id)
    if not read_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Заказа с этим id не найдено')
    return read_order


@router.get("/{user_id}",
            response_model=OrdersRead,
            status_code=status.HTTP_200_OK,
            summary='Получение заказов по id пользователя')
async def get_order_by_user_endpoint(db:db_session,user_id:int, payload:dict=Depends(require_roles('admin','manager','user'))):
    if payload.get('role')=='user' and payload.get('user_id')!=user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Нет доступа')
    read_order=await get_order_by_user(db,user_id)
    if not read_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Не найдены заказы')
    return read_order


@router.put("/", response_model=OrderRead,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_roles('admin','manager'))],
            summary='Изменение заказа')
async def update_order_endpoint(db:db_session,order_id:int,request:OrderUpdate):
    new_order=await update_order(db,order_id,request)
    if not new_order:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Что-то пошло не так')
    return new_order
