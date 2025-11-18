from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.models import Role
from backend.app.schemas.role import RoleRead, RolesRead, RoleUpdate, RoleBase

async def get_role_by_name(db: AsyncSession, name: str):
    role=await db.execute(select(Role).where(Role.name == name))
    result=role.scalar_one_or_none()
    if result is None:
        return None
    return RoleRead.model_to_dict(result)

async def create_role(db:AsyncSession,new_role:RoleBase):
    old_role=await get_role_by_name(db,new_role.name)
    if old_role:
        return None
    role = Role(name=new_role.name, description=new_role.description)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return RoleRead.model_validate(role)

async def get_role_by_id(db:AsyncSession, id:int):
    role=await db.execute(select(Role).where(Role.id==id))
    result=role.scalars().first()
    if result is None:
        return None
    return RoleRead.model_validate(result)

async def get_role_by_part_name(db:AsyncSession, name_part:str):
    roles=await db.execute(select(Role).where(Role.name.ilike(f"%{name_part}%")))
    if not roles:
        return None
    result_roles=roles.scalars().all()
    result=[RoleRead.model_validate(role) for role in result_roles]
    return RolesRead(roles=result)

async def delete_role_by_id(db:AsyncSession, id:int):
    role=await db.execute(select(Role).where(Role.id==id))
    result=role.scalar_one_or_none()
    if result is None:
        return None
    await db.delete(role)
    await db.commit()
    await db.refresh(role)
    return RoleRead.model_validate(role)

async def update_role_by_id(db:AsyncSession, id:int,update_role:RoleUpdate):
    role_search = await db.execute(select(Role).where(Role.id == id))
    role=role_search.scalar_one_or_none()
    if role is None:
        return None
    role.name = update_role.name
    role.description = update_role.description
    await db.commit()
    await db.refresh(role)
    return RoleRead.model_validate(role)


