from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.schemas.order import OrderCreate, OrderRead
from backend.app.crud.order import create_order,get_order_by_id

router=APIRouter(prefix="/order", tags=["/v1/order"])

db_session=Annotated[AsyncSession, Depends(get_db)]

@router.post("/", response_model=OrderRead,
             status_code=status.HTTP_201_CREATED,
             summary="Создание нового заказа")
async def create_order_endpoint(db:db_session,request: OrderCreate):
    new_order=await create_order(db,request)
    return new_order


@router.get("/", response_model=list[OrderRead],
            status_code=status.HTTP_200_OK,
            summary='Получение заказа по id')

async def get_order_by_id_endpoint(db:db_session,id:int):
    read_order=await get_order_by_id(db,id)
    if not read_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Заказа с этим id не найдено')
    return read_order
