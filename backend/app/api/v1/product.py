from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from backend.app.db.session import get_db
from backend.app.schemas.product import ProductRead
from backend.app.crud.product import *
from backend.app.api.v1.dependencies import require_roles

router=APIRouter(prefix="/product", tags=["/v1/product"])

db_session=Annotated[AsyncSession,Depends(get_db)]

@router.get("/{product_id}",
            status_code=status.HTTP_200_OK,
            response_model=ProductRead,
            summary='Получение продукта по id')
async def get_product_endpoint(db:db_session,product_id:int):
    product=await get_product_by_id(db,product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователя с этим id не существует')
    return product


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             response_model=ProductRead,
             dependencies=[Depends(require_roles('admin','customer'))],
             summary='Создание нового товара')
async def create_product_endpoint(db:db_session,product:ProductCreate):
    read_product=await get_product_by_name(db,product.name)
    if read_product:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                          detail='Продукт с таким названием уже существует')
    new_product=await create_product(db,product)
    return new_product

@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=list[ProductRead],
            summary='Поиск продукта по названию')
async def get_product_by_name_endpoint(db:db_session,name:str):
    product=await search_products_by_name(db,name)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Нет таких продуктов')
    return product

@router.put("/{product_id}",
            status_code=status.HTTP_200_OK,
            response_model=ProductRead,
            dependencies=[Depends(require_roles('admin','customer'))],
            summary='Изменение продукта по id')
async def update_product_endpoint(db:db_session,product_id:int,product:ProductUpdate):
    up_product=await update_product(db,product_id,product)
    if not up_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Продукт не найден')
    return ProductRead.model_validate(up_product)

@router.delete("/{product_id}",
               status_code=status.HTTP_200_OK,
               response_model=ProductRead,
               dependencies=[Depends(require_roles('admin','customer'))],
               summary='Удаление продукта')
async def delete_product_endpoint(db:db_session,product_id:int):
    delete_product_from_db=await delete_product(db,product_id)
    if not delete_product_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Продукт не найден')
    return ProductRead.model_validate(delete_product_from_db)