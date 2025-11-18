from typing import Annotated

from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession


from backend.app.db.session import get_db
from backend.app.schemas.role import RoleRead
from backend.app.crud.role import *


router=APIRouter(prefix="/v1/roles", tags=["roles"])

db_session=Annotated[AsyncSession,Depends(get_db)]

@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=RoleRead,
            summary='Получение роли по id')
async def get_role_by_id_endpoint( db:db_session,id:int):
    role=await get_role_by_id(db,id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Не найден роль с данным id')
    return role

@router.get("/all",
            status_code=status.HTTP_200_OK,
            response_model=RolesRead,
            summary='Получение ролей по названию или его части')
async def get_role_by_name_endpoint( db:db_session,name:str):
    roles=await get_role_by_part_name(db,name)
    if roles is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Не найдено ролей с таким именем')
    return roles

@router.put("/",
            status_code=status.HTTP_200_OK,
            response_model=RoleRead,
            summary='Изменение роли по id')
async def put_role_by_id_endpoint( db:db_session,id:int,update_role:RoleUpdate):
    role=await update_role_by_id(db,id,update_role)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Не найден роль с данным id')
    return role

@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=RoleRead,
             summary='Создание роли')
async def post_role_by_id_endpoint( db:db_session,new_role:RoleBase):
    role=await create_role(db,new_role)
    if not role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Такая роль уже существует')
    return role


@router.delete("/",
               status_code=status.HTTP_202_ACCEPTED,
               response_model=RoleRead,
               summary='Удаление роли')
async def delete_role_by_id_endpoint( db:db_session,id:int):
    role=await delete_role_by_id(db,id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Не найден роль с данным id')
    return role
